---
description: このテンプレートセットは、プロジェクト/ハブ接続のためのマネージドID認証とパブリックインターネットアクセスを有効にした標準セットアップでAzure AIエージェントサービスを設定する方法を示しています。エージェントは顧客所有のシングルテナントの検索およびストレージリソースを使用します。このセットアップでは、これらのリソースに対する完全な制御と可視性を持つことができますが、使用量に応じたコストが発生します。
page_type: sample
products:
- azure
- azure-resource-manager
urlFragment: standard-agent
languages:
- bicep
- json
---
# 標準エージェントセットアップ

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json)

[![Visualize](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/visualizebutton.svg?sanitize=true)](http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json)

ハブ、プロジェクト、ストレージアカウント、Key Vault、AI サービス、および Azure AI Search のリソースが作成されます。AI サービス、AI 検索、および Azure Blob Storage アカウントは、認証のためにマネージド ID を使用してプロジェクト/ハブに接続され、eastus リージョンに gpt-4o-mini モデルがデプロイされます。

オプションとして、パラメータファイルにフルARMリソースIDを提供することで、既存のAIサービス/AOAI、AI Search、および/またはAzure Blob Storageリソースを使用できます：

- aiServiceAccountResourceId
- aiSearchServiceResourceId
- aiStorageAccountResourceId

既存のAzure OpenAIリソースを使用する場合は、パラメータファイルの`aiServiceAccountResourceId`および`aiServiceKind`パラメータを更新する必要があります。`aiServiceKind`パラメータは`AzureOpenAI`に設定する必要があります。

## リソース

| プロバイダーとタイプ | 説明 |
| - | - |
| `Microsoft.Resources/resourceGroups` | すべてのリソースがデプロイされるリソースグループ |
| `Microsoft.KeyVault/vaults` | Azure Machine Learningワークスペースに関連付けられたAzure Key Vaultインスタンス |
| `Microsoft.Storage/storageAccounts` | Azure Machine Learningワークスペースに関連付けられたAzure Storageインスタンス |
| `Microsoft.MachineLearningServices/workspaces` | Azure AIハブ（種類が「ハブ」のAzure Machine Learning RPワークスペース） |
| `Microsoft.MachineLearningServices/workspaces` | Azure AIプロジェクト（種類が「プロジェクト」のAzure Machine Learning RPワークスペース） |
| `Microsoft.CognitiveServices/accounts` | モデル・アズ・ア・サービスのエンドポイントプロバイダーとしてのAzure AIサービス（許可される種類：'AIServices'および'OpenAI'） |
| `Microsoft.CognitiveServices/accounts/deployments` | gpt-4o-miniモデルがデプロイされます |
| `Microsoft.Search/searchServices` | Azure AI検索アカウント |
`Tags: `