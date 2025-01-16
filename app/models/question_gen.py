import google.generativeai as genai


genai.configure(api_key="AIzaSyCxgKo5NcdNFLRsdenH3vny_dMiEFszfjo")
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_questions(resume_content, jd_content):

    #  input prompt
    prompt = (
        f"Analyze the following resume and job description to generate questions for screening candidates. "
        f"Focus on skills that align in both the resume and job description. Create 4-5 questions, "
        f"starting from basic to tricky level.\n\n"
        f"Resume Content:\n{resume_content}\n\n"
        f"Job Description:\n{jd_content}\n"
    )

    try:
        # Send request to the Gemini model
        response = model.generate_content(prompt)
        
        # Extract the generated content
        generated_text = response.text if hasattr(response, 'text') else str(response)
        
        # Split the generated text into individual questions (if they are listed)
        questions = [q.strip() for q in generated_text.split('\n') if q.strip()]

        return questions

    except Exception as e:
        print(f"Error generating questions: {e}")
        return []



