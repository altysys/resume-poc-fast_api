from config import DEPLOYMENT_NAME
import openai
def feed_back(resume_content, jd_content):
    try:
        prompt = (
            f"Resume Summary:\n{resume_content}\n\n"
            f"Job Description:\n{jd_content}\n\n"
            f"Answer the following:\n"
            f"1. Skill alignment percentage (in key-value pair)\n"
            f"2. Key technical skills missing from resume but present in JD (in key-value pair)\n"
            f"3. How do missing skills affect candidacy? (short analysis)\n"
            f"4. Based on experience, skills, and projects, is this candidate fit for the role? (key-value pair: Yes/No)\n"
            f"5. Provide final selection feedback explaining why candidate should or shouldn't be selected (in key-value pairs).\n\n"
            f"Respond strictly in JSON format with key-value pairs only."
        )

        response = openai.ChatCompletion.create(
    deployment_id=DEPLOYMENT_NAME,            messages=[
                {"role": "system", "content": "You are a resume evaluation assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error in analyzing resume: {e}")
        return "An error occurred while analyzing the resume."
