from pathlib import Path
from dotenv import load_dotenv, dotenv_values

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)
values_env = dotenv_values(env_path)
AZURE_OPENAI_ENDPOINT = values_env["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_DEPLOYMENT_ID = values_env["AZURE_OPENAI_DEPLOYMENT_ID"]

