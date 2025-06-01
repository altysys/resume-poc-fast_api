import re
import json
from config import DEPLOYMENT_NAME
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import openai

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    if isinstance(text, list):
        text = ' '.join(text)
    if not isinstance(text, str):
        raise ValueError("Input must be a string or a list of strings.")
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in text.split() if word not in stop_words]
    return ' '.join(filtered_words)


def use_openai_llm(summary, jd_content):
    prompt = (
        f"Analyze the following resume summary and job description thoroughly. "
        f"Provide the following information in JSON format:\n\n"
        f"{{\n"
        f"  \"name\": \"<Candidate Name>\",\n"
        f"  \"email\": \"<Candidate Email>\",\n"
        f"  \"SkillMatchScore\": <score from 0 to 100>,\n"
        f"  \"YearsExperienceRequired\": <years from JD>,\n"
        f"  \"CandidateExperience\": <years from resume>\n"
        f"}}\n\n"
        f"Resume Summary:\n{summary}\n\n"
        f"Job Description:\n{jd_content}"
    )

    try:
        response = openai.ChatCompletion.create(
            deployment_id=DEPLOYMENT_NAME,  # ✅ Correct for Azure OpenAI
            messages=[
                {"role": "system", "content": "You are an expert resume screening assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=5000
        )

        # ✅ Azure OpenAI returns response.choices[0].message["content"]
        content = response.choices[0].message["content"].strip()

        # Attempt to extract JSON block from the response
        json_match = re.search(r'\{[\s\S]*?\}', content)
        if not json_match:
            raise ValueError("No valid JSON found in model response.")
        
        parsed_data = json.loads(json_match.group(0))

        return {
            "skill_match_score": int(parsed_data.get("SkillMatchScore", 0)),
            "name": parsed_data.get("name", "N/A"),
            "email": parsed_data.get("email", "N/A"),
            "jd_experience": parsed_data.get("YearsExperienceRequired", "N/A"),
            "resume_experience": parsed_data.get("CandidateExperience", "N/A")
        }

    except Exception as e:
        print(f"Error in OpenAI LLM: {e}")
        return {
            "skill_match_score": 0,
            "name": "N/A",
            "email": "N/A",
            "jd_experience": "N/A",
            "resume_experience": "N/A"
        }


def score_resume(resume_summary, job_description):
    results = use_openai_llm(resume_summary, job_description)
    final_score = results.get("skill_match_score", 0)
    alignment = final_score  # you may change this logic if needed
    print("Results:", results)
    return final_score, alignment
