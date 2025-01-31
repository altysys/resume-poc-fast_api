import requests
import google.generativeai as genai

# Replace with your Gemini API key


# Configure the GenAI client
genai.configure(api_key=GEMINI_API_KEY)

def summarize_resume(resume_content):
    try:
        # Initialize the generative model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Generate a summary
        response = model.generate_content(f"find out email and name from the resume if available " 
                                          f"year of experience in resume"
                                          f"Summarize this resume:\n\n{resume_content}"
                                          f"proveide response in proper json format in key value pairs ")
        
        # Extract and return the text
        return response.text.strip()
    except Exception as e:
        print(f"Error in summarizing resume: {e}")
        return "An error occurred while summarizing the resume."
