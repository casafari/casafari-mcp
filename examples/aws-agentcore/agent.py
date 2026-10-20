"""Ask Casafari a question through the AgentCore Gateway that setup_gateway.py created.

    python agent.py
    python agent.py "How have asking prices per m2 of flats in Porto moved over the last two years?"

A Strands Agents agent on an Amazon Bedrock model lists the gateway's tools and calls the ones the
question needs. The gateway is called with your IAM credentials (SigV4, mcp-proxy-for-aws) and
calls Casafari with the key it keeps in AgentCore Identity: no Casafari key is needed here.
"""
import os
import sys

import boto3
from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

GATEWAY_URL = os.environ.get("CASAFARI_GATEWAY_URL") or sys.exit("Set CASAFARI_GATEWAY_URL (setup_gateway.py prints it).")
REGION = os.environ.get("AWS_REGION") or boto3.Session().region_name or sys.exit("Set AWS_REGION to the gateway's Region.")
QUESTION = " ".join(sys.argv[1:]) or (
    "What is a 2-bedroom flat of 85 m² near Avenida da Liberdade, Lisbon worth? Use comparables within 1 km."
)
SYSTEM = (
    "You answer real estate questions with Casafari's tools. When a tool needs a location id, find it "
    "with the locations tools first. Give every figure with its unit and what it rests on, and say so "
    "when the data does not state something."
)

# BEDROCK_MODEL_ID: a model or inference profile your account can use in this Region, for example an
# EU inference profile to keep inference in the EU. Without it, Strands Agents uses its default model
# (a global cross-Region inference profile of Claude Sonnet in strands-agents 1.61).
model_id = os.environ.get("BEDROCK_MODEL_ID")
model = BedrockModel(model_id=model_id, region_name=REGION) if model_id else BedrockModel(region_name=REGION)

gateway = MCPClient(lambda: aws_iam_streamablehttp_client(
    endpoint=GATEWAY_URL,
    aws_region=REGION,
    aws_service="bedrock-agentcore",
    timeout=120,  # seconds per request; some tools take longer than the default 30
))

with gateway:
    tools, token = [], None
    while True:  # the gateway may return its tools in pages
        page = gateway.list_tools_sync(pagination_token=token)
        tools += page
        token = page.pagination_token
        if not token:
            break
    print(f"{len(tools)} tools: {', '.join(t.tool_name for t in tools)}\n", file=sys.stderr)
    agent = Agent(model=model, tools=tools, system_prompt=SYSTEM)
    agent(QUESTION)  # streams the answer to stdout
    print()
