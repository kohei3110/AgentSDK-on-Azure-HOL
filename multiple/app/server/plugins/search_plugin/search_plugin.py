import os
from typing import Annotated
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from semantic_kernel.functions.kernel_function_decorator import kernel_function

from services.search_agent_service import SearchAgentService


class SearchPlugin:
    """
    Description: SearchPlugin provides a set of functions to search items by Bing.

    Usage:
        kernel.import_plugin_from_object(SearchPlugin(), plugin_name="search")
    """

    @kernel_function(name="search", description="Search for items by Bing.")
    def search(
        self,
        search_item: Annotated[str, "the subject of the email"],
    ) -> Annotated[str, "the output is a string"]:
        """Search for items by Bing."""
        project_client: AIProjectClient = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
        )

        search_agent_service = SearchAgentService(project_client)
        response = search_agent_service.search(search_item)

