from fastapi import APIRouter, Depends
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings, OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig

from plugins.search_plugin.services import search_agent_service
from services.service_settings import ServiceSettings
from services.services import Service


router = APIRouter()

@router.get("/search")
def search(
    company_name: str,
    search_agent_service: search_agent_service.SearchAgentService = Depends(search_agent_service)
):

    kernel: Kernel = Kernel()
    service_settings: ServiceSettings = ServiceSettings.create()
    selectedService: Service = (
        Service.AzureOpenAI
        if service_settings.global_llm_service is None
        else Service(service_settings.global_llm_service.lower())
    )
    service_id = None
    if selectedService == Service.OpenAI:
        service_id = "default"
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
            ),
        )
        execution_settings = OpenAIChatPromptExecutionSettings(
            service_id=service_id,
            ai_model_id="gpt-3.5-turbo",
            max_tokens=2000,
            temperature=0.7,
        )
    elif selectedService == Service.AzureOpenAI:
        service_id = "default"
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
            ),
        )
        execution_settings = AzureChatPromptExecutionSettings(
            service_id=service_id,
            ai_model_id="gpt-4o-mini",
            max_tokens=2000,
            temperature=0.7,
        )


    prompt = """
    あなたは3C分析を専門とするアシスタントです。3Cフレームワーク（Company, Customer, Competitor）を用いて、指定された企業についての分析を行い、情報を簡潔に整理して提供してください。以下の指示に従ってください：

    1. **目的**  
    {{$company_name}}について3C分析を行い、以下を明確にする：  
    - **Company（自社）**: 企業の強み、弱み、機会、脅威（SWOT分析を含む）。  
    - **Customer（顧客）**: 企業のターゲット顧客層、顧客ニーズ、行動傾向。  
    - **Competitor（競合）**: 主な競合他社、競合の戦略や市場でのポジショニング。

    2. **使用ツール**  
    Bing Search APIを使用して、指定された企業に関する最新情報を検索し、分析に必要な情報を収集してください。特に以下の情報を優先します：
    - 企業の公式ウェブサイト、ニュース、業界レポート。
    - 顧客のレビューや行動傾向に関するデータ。
    - 主な競合他社の戦略や市場での動き。

    3. **手順**  
    - 指定された企業に関する概要情報を検索し、基本的な背景情報を収集する。  
    - さらに、3Cごとに以下の詳細情報を収集する：  
        - **Company**: 製品・サービス、マーケティング戦略、最近の業績や発表。  
        - **Customer**: 顧客層、ニーズ、購買行動、市場トレンド。  
        - **Competitor**: 主な競合他社のリスト、戦略、競争優位性。  
    - 収集した情報を3Cに分類し、簡潔でわかりやすいフォーマットで出力する。
    """

    prompt_template_config = PromptTemplateConfig(
        template=prompt,
        name="story",
        template_format="semantic-kernel",
        input_variables=[
            InputVariable(name="company_name", description="企業名", is_required=True),
        ],
        execution_settings=execution_settings,
    )

    bing_search = kernel.add_plugin(
        
    )