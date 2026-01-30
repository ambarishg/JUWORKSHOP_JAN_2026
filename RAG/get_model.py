from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

try:
    from .config import *
except ImportError:  # script run outside package context
    from config import *

project = AIProjectClient(
    endpoint=AZURE_OPENAI_ENDPOINT,
    credential=DefaultAzureCredential(),
)

client = project.get_openai_client(api_version="2024-10-21")

MODEL_NAME = AZURE_OPENAI_DEPLOYMENT_ID
