# from config import client, DEPLOYMENT_NAME  # assumes config.py is properly set

# def generate_questions(resume_content, jd_content):
#     # Input prompt
#     prompt = (
#         f"Analyze the following resume and job description to generate screening questions. "
#         f"Focus on overlapping and key technical skills. Create 4–5 questions with detailed key point answers. "
#         f"The questions should progress from basic to advanced level.\n\n"
#         f"Resume Content:\n{resume_content}\n\n"
#         f"Job Description:\n{jd_content}\n\n"
#         f"Return the questions and answers clearly formatted in JSON as an array of objects like:\n"
#         f"[{{\"question\": \"...\", \"answer\": \"...\"}}, ...]"
#     )

#     try:
#         # Send request to Azure OpenAI
#         response = client.chat.completions.create(
#             model=DEPLOYMENT_NAME,
#             messages=[
#                 {"role": "system", "content": "You are a technical recruiter AI assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.7,
#             max_tokens=1000
#         )

#         content = response.choices[0].message.content.strip()

#         # Optional: Try parsing as JSON (if OpenAI returns valid JSON)
#         import json
#         try:
#             return json.loads(content)
#         except json.JSONDecodeError:
#             return content  # fallback to raw string if JSON is malformed

#     except Exception as e:
#         print(f"Error generating questions: {e}")
#         return []
