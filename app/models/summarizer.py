from config import DEPLOYMENT_NAME
import openai
import json
import re

def summarize_resume(resume_content):
    prompt = (
        f"Analyze the resume below and provide a structured JSON response with:\n"
        f"{{\n"
        f"  \"name\": \"<Candidate Name>\",\n"
        f"  \"email\": \"<Candidate Email>\",\n"
        f"  \"years_experience\": <Years of Experience>,\n"
        f"  \"summary\": \"<Concise Summary>\"\n"
        f"}}\n\n"
        f"Resume:\n{resume_content}"
    )

    try:
        response = openai.ChatCompletion.create(
             deployment_id=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a resume summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=5000
        )

        content = response.choices[0].message["content"].strip()
        json_match = re.search(r'\{[\s\S]*?\}', content)

        if json_match:
            return json.loads(json_match.group(0))
        else:
            raise ValueError("JSON not found in model output")

    except Exception as e:
        print(f"Error summarizing resume: {e}")
        return {
         {
  "name": "...",
  "email": "...",
  "years_experience": "...",
  "summary": "..."
}
        }
