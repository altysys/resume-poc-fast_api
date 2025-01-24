import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import requests
import google.generativeai as genai
import json

# Ensure you download NLTK stopwords first
nltk.download('stopwords')

def preprocess_text(text):
    """Preprocess text by removing special characters, stopwords, and normalizing case."""
    import re
    from nltk.corpus import stopwords

    # Check if input is a list
    if isinstance(text, list):
        # Join the list into a single string
        text = ' '.join(text)

    # Ensure input is now a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string or a list of strings.")

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)


def use_gemini_llm(summary, jd_content):
    # Define the Gemini API endpoint and headers
    genai.configure(api_key="AIzaSyCxgKo5NcdNFLRsdenH3vny_dMiEFszfjo")
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Prepare the input as a single string
    input_text = (
    f"Analyze the following resume summary and job description thoroughly. "
    f"Provide the following information explicitly:\n"
    f"1. A Skill Match Score (0-100) based on the alignment between the resume and the job description. in this format SkillMatchScore : score \n"
    f"2. A the job description explicitly requires how many yrs of experince  ?\n"
    f"3. candidate resume demonstrates how many yrs of experince in number in this format resume_experience :  \n"
    f"Resume Summary:\n{summary}\n\n"
    f"Job Description:\n{jd_content}"
    f"create proper key value pair for score , year of experince , email and name in proper json format very imp "
      )

    #print("here we go for debbugunh " , input_text)   
    response = model.generate_content(input_text)
    json_response = json.dumps({"text": response.text}, indent=2)  # Embed in JSON
    print("json_response" , json_response)
   

    json_match = re.search(r'```json\\n(.*?)\\n```', json_response, re.DOTALL)

    if json_match:
    # Step 2: Clean up the JSON string
        json_data = json_match.group(1).replace('\\n', '').replace('\\', '')

    try:
        # Step 3: Parse the JSON data
        parsed_data = json.loads(json_data)

        # Step 4: Extract required fields
        email = parsed_data.get("email", "N/A")
        name = parsed_data.get("name", "N/A")
        skill_match_score = parsed_data.get("SkillMatchScore", 0)
        job_description_experience_requirement = parsed_data.get("YearsExperienceRequired", "N/A")
        candidate_experience = parsed_data.get("ArchitsYearsExperience", "N/A")

        # Step 5: Print the extracted details
        print(f"Email josn: {email}")
        print(f"Name josn: {name}")
        print(f"Skill Match Score json: {skill_match_score}")
        print(f"Job Description Experience Requirement json: {job_description_experience_requirement}")
        print(f" Experience json : {candidate_experience}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    else:
        print("JSON block not found in the response.")



  



# Create gemini_result object
    gemini_result = {
        "skill_match_score": skill_match_score,
    }
    print("hger" , gemini_result)

    return gemini_result



def score_resume(resume_summary, job_description):
    """Score the resume summary against the job description."""
    # Preprocess the text
    # Use Gemini LLM for advanced skill and experience matching
    gemini_results = use_gemini_llm(resume_summary, job_description)
    
    # Combine the baseline and Gemini LLM results
    final_score = (gemini_results["skill_match_score"])
    alignment =   final_score
    return final_score, alignment