import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPEN_API_KEY")
        self.endpoint = os.getenv("LLM_ENDPOINT")
        self.deployment_name = os.getenv("LLM_NAME")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
        # Validate required environment variables
        if not all([self.api_key, self.endpoint, self.deployment_name]):
            raise ValueError(
                "Missing required environment variables. Please ensure OPEN_API_KEY, "
                "LLM_ENDPOINT, and LLM_NAME are set."
            )
        
        # Ensure endpoint has proper scheme
        if not self.endpoint.startswith(('http://', 'https://')):
            self.endpoint = f"https://{self.endpoint}"
        
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def generate_response(self, prompt, max_tokens=15000, temperature=0.7):
        """
        Sends a completion request to Azure OpenAI. 
        """
        url = f"{self.endpoint}openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an AI assistant that generates high-quality multiple-choice questions based on provided content."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "temperature": temperature,
            "top_p": 0.95,
            "max_tokens": max_tokens
        }

        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()
            try:
                content = response_data['choices'][0]['message']['content']
                return json.loads(content)
            except json.JSONDecodeError:
                return response_data['choices'][0]['message']['content']
        else:
            return {"error": f"Failed with status code {response.status_code}"}

 