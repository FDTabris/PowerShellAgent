import os
import json
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

endpoint = config.get("endpoint")
# model_name = config.get("model_name")
deployment = config.get("deployment")
api_version = config.get("api_version")
# For Azure OpenAI, an API key is typically required.
# If you want to avoid using a key, you would need to use Azure Active Directory (AAD) authentication.
# The openai-python library supports AAD via the 'azure_ad_token' parameter.
# Example (requires 'azure-identity' library):


token_provider = get_bearer_token_provider(
    # InteractiveBrowserCredential(),
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

# Pass the token to the client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?",
        }
    ],
    max_completion_tokens=800,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=deployment
)

print(response.choices[0].message.content)