import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from plugins.search_plugin.services.search_agent_service import SearchAgentService

load_dotenv()

app: FastAPI = FastAPI(
    title="API Sample for Agent SDK",
    description="API for Agent SDK",
    version="1.0.0",
)

project_client: AIProjectClient = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

search_agent_service = SearchAgentService(project_client)

import controllers.controller as controller
app.include_router(controller.router)