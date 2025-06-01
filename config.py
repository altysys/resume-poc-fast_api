# config.py

import os
from dotenv import load_dotenv
import openai

load_dotenv()

# Load Azure OpenAI credentials
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")  # Your Azure OpenAI API key
OPENAI_API_BASE = os.getenv("LLM_ENDPOINT")  # Should be like: https://<your-resource-name>.openai.azure.com/
OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")  # e.g., "2024-02-15-preview"
DEPLOYMENT_NAME = os.getenv("LLM_NAME")  # Your deployment name for GPT model

# Configure OpenAI client globally
openai.api_type = "azure"
openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE
openai.api_version = OPENAI_API_VERSION
