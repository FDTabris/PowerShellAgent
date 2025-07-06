from azure.identity import AzureCliCredential

credential = AzureCliCredential()
token = credential.get_token("https://management.azure.com/.default")
print(token.token)