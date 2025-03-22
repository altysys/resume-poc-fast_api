import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, api_key, endpoint, deployment_name, api_version="2024-02-15-preview"):
        """
        Initializes the Azure OpenAI Async Client.
       
        Args:
            api_key (str): Your Azure API key.
            endpoint (str): Azure OpenAI endpoint URL.
            deployment_name (str): Name of the model deployment in Azure.
            api_version (str): API version to use.
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.deployment_name = deployment_name
        self.api_version = api_version
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

    