"""Put Casafari's property-data MCP servers behind an Amazon Bedrock AgentCore Gateway.

Creates, in your AWS account and Region:

  1. an API key credential provider in AgentCore Identity that holds CASAFARI_API_KEY (cf_sk_...),
  2. an IAM role the gateway assumes to read that key,
  3. a gateway whose callers sign in with their IAM credentials (SigV4),
  4. one MCP server target per Casafari server; each sends the key as X-API-Key.

    python setup_gateway.py            # create, or reuse what exists (re-running updates the stored key)
    python setup_gateway.py --delete   # remove everything this script created

The key is read from the environment. It is never printed and never written to disk.
"""
import argparse
import json
import os
import sys
import time

import boto3
from botocore.exceptions import ClientError

NAME = os.environ.get("CASAFARI_GATEWAY_NAME", "casafari")
ROLE = f"{NAME}-agentcore-gateway"
# Target name -> Casafari MCP server. The gateway calls each tool "<target>___<tool>", and an Amazon
# Bedrock model takes tool names of at most 64 characters, so target names stay this short:
# "area-insights___area-insights_get_time_on_market_distribution" is 61.
TARGETS = {
    "locations": "https://platform.casafari.com/mcp/locations",
    "comparables": "https://platform.casafari.com/mcp/comparables",
    "area-insights": "https://platform.casafari.com/mcp/area-insights",
    # Claro AI (commercial premises in Spain, commercial plots in Germany) works the same way:
    # "claro": "https://platform.casafari.com/mcp/claro",
}
FAILED = {"FAILED", "UPDATE_UNSUCCESSFUL", "SYNCHRONIZE_UNSUCCESSFUL"}

REGION = os.environ.get("AWS_REGION") or boto3.Session().region_name
if not REGION:
    sys.exit("Set AWS_REGION (or a default Region in your AWS profile).")
session = boto3.Session(region_name=REGION)
ctl = session.client("bedrock-agentcore-control")
iam = session.client("iam")


def code(e: ClientError) -> str:
    return e.response["Error"]["Code"]


def wait_for(get, what: str, done=("READY",), minutes: int = 10) -> dict:
    """Poll get() until its status is done; stop on a failed status."""
    for _ in range(minutes * 12):
        r = get()
        if r["status"] in done:
            return r
        if r["status"] in FAILED:
            sys.exit(f"{what}: {r['status']} {r.get('statusReasons', '')}")
        time.sleep(5)
    sys.exit(f"{what}: still {r['status']} after {minutes} minutes")


def find_gateway() -> dict | None:
    kw = {}
    while True:
        page = ctl.list_gateways(**kw)
        for g in page.get("items", []):
            if g["name"] == NAME:
                return g
        if not page.get("nextToken"):
            return None
        kw["nextToken"] = page["nextToken"]


def list_targets(gateway_id: str) -> list[dict]:
    items, kw = [], {"gatewayIdentifier": gateway_id}
    while True:
        page = ctl.list_gateway_targets(**kw)
        items += page.get("items", [])
        if not page.get("nextToken"):
            return items
        kw["nextToken"] = page["nextToken"]


def credential_provider() -> tuple[str, str]:
    """The API key credential provider holding the Casafari key: its ARN and its secret's ARN."""
    key = os.environ.get("CASAFARI_API_KEY", "")
    if not key.startswith("cf_sk_"):
        sys.exit("Set CASAFARI_API_KEY to a Casafari platform API key (cf_sk_...) from https://platform.casafari.com/console/")
    try:
        r = ctl.create_api_key_credential_provider(name=NAME, apiKey=key)
        print(f"credential provider {NAME}: created")
    except ClientError as e:
        if code(e) not in ("ConflictException", "ValidationException") or "exist" not in str(e).lower():
            raise
        r = ctl.update_api_key_credential_provider(name=NAME, apiKey=key)
        print(f"credential provider {NAME}: key updated")
    return r["credentialProviderArn"], r["apiKeySecretArn"]["secretArn"]


def gateway_role(provider_arn: str, secret_arn: str) -> str:
    """An IAM role AgentCore can assume, allowed to read the Casafari key and nothing else."""
    account = session.client("sts").get_caller_identity()["Account"]
    partition = provider_arn.split(":")[1]
    trust = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
            "Action": "sts:AssumeRole",
            "Condition": {"StringEquals": {"aws:SourceAccount": account}},
        }],
    }
    directory = f"arn:{partition}:bedrock-agentcore:{REGION}:{account}:workload-identity-directory/default"
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {"Sid": "WorkloadAccessToken", "Effect": "Allow", "Action": "bedrock-agentcore:GetWorkloadAccessToken",
             "Resource": [directory, f"{directory}/workload-identity/{NAME}-*"]},
            {"Sid": "CasafariApiKey", "Effect": "Allow", "Action": "bedrock-agentcore:GetResourceApiKey",
             "Resource": [provider_arn.split("/apikeycredentialprovider/")[0], provider_arn]},
            {"Sid": "CasafariApiKeySecret", "Effect": "Allow", "Action": "secretsmanager:GetSecretValue", "Resource": secret_arn},
        ],
    }
    try:
        arn = iam.create_role(RoleName=ROLE, AssumeRolePolicyDocument=json.dumps(trust),
                              Description="AgentCore Gateway for Casafari: reads the Casafari API key")["Role"]["Arn"]
        print(f"role {ROLE}: created")
    except ClientError as e:
        if code(e) != "EntityAlreadyExists":
            raise
        arn = iam.get_role(RoleName=ROLE)["Role"]["Arn"]
    iam.put_role_policy(RoleName=ROLE, PolicyName="casafari-api-key", PolicyDocument=json.dumps(policy))
    return arn


def gateway(role_arn: str) -> dict:
    g = find_gateway()
    if not g:
        for attempt in range(13):
            try:
                g = ctl.create_gateway(
                    name=NAME,
                    roleArn=role_arn,
                    protocolType="MCP",
                    authorizerType="AWS_IAM",
                    description="Casafari property data: Location Lookup, Comparables, Area Insights",
                )
                print(f"gateway {NAME}: created")
                break
            except ClientError as e:
                # A role created a moment ago can take a few seconds before AgentCore may assume it.
                if code(e) == "ValidationException" and "role" in str(e).lower() and attempt < 12:
                    time.sleep(5)
                    continue
                raise
    return wait_for(lambda: ctl.get_gateway(gatewayIdentifier=g["gatewayId"]), f"gateway {NAME}")


def targets(gateway_id: str, provider_arn: str) -> None:
    existing = {t["name"]: t["targetId"] for t in list_targets(gateway_id)}
    credential = [{
        "credentialProviderType": "API_KEY",
        "credentialProvider": {"apiKeyCredentialProvider": {
            "providerArn": provider_arn,
            "credentialLocation": "HEADER",
            "credentialParameterName": "X-API-Key",
        }},
    }]
    for name, url in TARGETS.items():
        target_id = existing.get(name)
        if not target_id:
            target_id = ctl.create_gateway_target(
                gatewayIdentifier=gateway_id,
                name=name,
                description=f"Casafari MCP server {url}",
                targetConfiguration={"mcp": {"mcpServer": {"endpoint": url}}},
                credentialProviderConfigurations=credential,
            )["targetId"]
        # On creation the gateway calls the server's tools/list with the key: a bad key fails here.
        wait_for(lambda: ctl.get_gateway_target(gatewayIdentifier=gateway_id, targetId=target_id), f"target {name}")
        print(f"target {name}: ready")


def delete() -> None:
    g = find_gateway()
    if g:
        gid = g["gatewayId"]
        for t in list_targets(gid):
            ctl.delete_gateway_target(gatewayIdentifier=gid, targetId=t["targetId"])
        for _ in range(60):
            if not list_targets(gid):
                break
            time.sleep(5)
        ctl.delete_gateway(gatewayIdentifier=gid)
        print(f"gateway {NAME}: deleted")
    try:
        iam.delete_role_policy(RoleName=ROLE, PolicyName="casafari-api-key")
        iam.delete_role(RoleName=ROLE)
        print(f"role {ROLE}: deleted")
    except ClientError as e:
        if code(e) != "NoSuchEntity":
            raise
    try:
        ctl.delete_api_key_credential_provider(name=NAME)
        print(f"credential provider {NAME}: deleted")
    except ClientError as e:
        if code(e) != "ResourceNotFoundException":
            raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--delete", action="store_true", help="remove the gateway, its targets, the role and the stored key")
    if parser.parse_args().delete:
        delete()
        return
    provider_arn, secret_arn = credential_provider()
    g = gateway(gateway_role(provider_arn, secret_arn))
    targets(g["gatewayId"], provider_arn)
    print("\nNext:")
    print(f"  export AWS_REGION={REGION}")
    print(f"  export CASAFARI_GATEWAY_URL={g['gatewayUrl']}")
    print("  python agent.py")


if __name__ == "__main__":
    main()
