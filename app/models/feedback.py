import requests
import google.generativeai as genai

# Replace with your Gemini API key
GEMINI_API_KEY = "AIzaSyCxgKo5NcdNFLRsdenH3vny_dMiEFszfjo"

# Configure the GenAI client
genai.configure(api_key=GEMINI_API_KEY)

def feed_back(resume_content , jd_content):
    try:
        # Initialize the generative model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Generate a summary
        response = model.generate_content( f"Resume Summary:\n{resume_content}\n\n"
                                           f"Job Description:\n{jd_content}"
                                           f"How much percent skills aligned with job description skill in key value pair"
                                           f"what key-skill(technical skills important for job role) not present in resume but present in job descriptin in key value pair"
                                           f"analyse properly how much missing skills affect the candidancy of resume accordinng to job_decription and make response according "
                                           f"On basis of resume analysis seeing experince and skill and projects is this candidate fit for the job provided in job description analyse properly and provide answer in key value pair in yes or no clearly " 
                                           f"provide feedback on basis of  slection asked before and resume and job description why need to selected why not selected in key value pair condider experince and skills involded"
                                           f"provide response in proper json format in key value pairs must answer all the questions")
        
        # Extract and return the text
        return response.text.strip()
    except Exception as e:
        print(f"Error in summarizing resume: {e}")
        return "An error occurred while summarizing the resume."
