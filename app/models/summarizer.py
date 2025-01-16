import requests
import google.generativeai as genai

# Replace with your Gemini API key
GEMINI_API_KEY = "AIzaSyCxgKo5NcdNFLRsdenH3vny_dMiEFszfjo"

# Configure the GenAI client
genai.configure(api_key=GEMINI_API_KEY)

def summarize_resume(resume_content):
    try:
        # Initialize the generative model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Generate a summary
        response = model.generate_content(f"Summarize this resume:\n\n{resume_content}")
        
        # Extract and return the text
        return response.text.strip()
    except Exception as e:
        print(f"Error in summarizing resume: {e}")
        return "An error occurred while summarizing the resume."
