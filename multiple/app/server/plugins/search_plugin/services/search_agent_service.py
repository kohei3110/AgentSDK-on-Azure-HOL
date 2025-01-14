import time
from typing import Set

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import Agent, AgentThread, BingGroundingTool, ConnectionProperties, RunStatus, MessageRole, MessageTextContent, ToolSet

from plugins.search_plugin.tools.knowledge.bing_grounding_tool import create_bing_grounding_tool

class SearchAgentService:

    def __init__(self, project_client: AIProjectClient):
        self.project_client = project_client

    def search(self, search_item: str) -> str:
        agent, thread = self.create_agent_and_thread()
        run = self.run(user_message=search_item, agent=agent, thread=thread)

        while run.status in [RunStatus.QUEUED, RunStatus.IN_PROGRESS, RunStatus.REQUIRES_ACTION]:
            time.sleep(1)
            run = self.project_client.agents.get_run(thread_id=thread.id, run_id=run.id)
            logger.info(f"Current run status1: {run.status}")

            if run.status == RunStatus.REQUIRES_ACTION:
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    self.project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                    break

                tool_outputs = self.execute_tool_calls(tool_calls)

                print(f"Tool outputs: {tool_outputs}")
                if tool_outputs:
                    self.project_client.agents.submit_tool_outputs_to_run(
                        thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                    )
                else:
                    print("No tool outputs to submit - cancelling run")
                    self.project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                    break

            print(f"Current run status2: {run.status}")

        print(f"Run completed with status: {run.status}")

        assistant_messages = self.get_assistant_responses(thread)
        return {"response": assistant_messages[0]}    
    
    def create_agent_and_thread(self):

        toolset: ToolSet = ToolSet()

        bing_grounding_connection: ConnectionProperties = self.project_client.connections.get(
            connection_name="bing_search"
        )
        bing_grounding_tool: BingGroundingTool = create_bing_grounding_tool(connection_id=bing_grounding_connection.id)
        toolset.add(bing_grounding_tool)

        thread = self.project_client.agents.create_thread()
        agent: Agent = self.project_client.agents.create_agent(
            model="gpt-35-turbo",
            name="SearchAgent",
            instructions="""
            あなたは3C分析を行う際、対象企業を分析するのに役立つ最新情報を検索するアシスタントです。
            あなたは以下の業務を遂行します。
            - 指定された企業について、最新情報を収集するための検索を、Bing Groundingを使用して実行します（例: 企業ニュース、公式ウェブサイト、最近の発表、業界レポートなど）。

            #制約事項
            - ユーザーからのメッセージは日本語で入力されます
            - ユーザーからのメッセージから忠実に情報を抽出し、それに基づいて応答を生成します。
            - ユーザーからのメッセージに勝手に情報を追加したり、不要な改行文字 \n を追加してはいけません
            """,
            toolset=toolset,
            headers={"x-ms-enable-preview": "true"},
        )
        print(f"Created agent: {agent}")
        return agent, thread

    def run(self, user_message: str, agent: Agent, thread: AgentThread):
        self.project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=user_message,
        )
        return self.project_client.agents.create_run(thread_id=thread.id, assistant_id=agent.id)

    tool_outputs = [self.project_client.tools.execute_tool_call(tool_call) for tool_call in tool_calls]
        print(f"Requires more information to continue: {tool_calls}")

    def get_assistant_responses(self, thread: AgentThread):
        agent_messages = self.project_client.agents.list_messages(thread_id=thread.id)
        assistant_messages = []
        for data_point in reversed(agent_messages.data):
            last_message_content = data_point.content[-1]
            if isinstance(last_message_content, MessageTextContent):
                print(f"{data_point.role}: {last_message_content.text.value}")
                if data_point.role == MessageRole.AGENT:
                    assistant_messages.append(last_message_content.text.value)
        return assistant_messages
