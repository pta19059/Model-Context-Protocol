
# Azure AI Foundry Setup Script
# Esegui manualmente questi comandi se desideri

# 1. Verifica regioni supportate per AI Foundry
az provider show --namespace Microsoft.CognitiveServices --query "resourceTypes[?resourceType=='accounts'].locations | [0]"

# 2. Crea risorsa Azure OpenAI (se non esiste)
az cognitiveservices account create --name oai-kfqy2u --resource-group rg-mcp-kfqy2u --location eastus --kind OpenAI --sku s0

# 3. Vai su https://ai.azure.com
# 4. Crea nuovo Hub
# 5. Seleziona subscription e resource group: rg-mcp-kfqy2u
# 6. Collega a OpenAI: oai-kfqy2u
# 7. Crea nuovo agente
# 8. Aggiungi funzione personalizzata usando: openapi-weather.json
