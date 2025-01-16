import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import requests
import google.generativeai as genai


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
    f"1. A Skill Match Score (0-100) based on the alignment between the resume and the job description.\n"
    f"2. A the job description explicitly requires how many yrs of experince  ?\n"
    f"3. Archit's resume demonstrates how many yrs of experince ? \n"
    f"Resume Summary:\n{summary}\n\n"
    f"Job Description:\n{jd_content}"
      )

    #print("here we go for debbugunh " , input_text)   
    response_text = model.generate_content(input_text)
    print("debugger", response_text)
# Extract the generated text content
    try:
        response_get = response_text.candidates[0].content.parts[0].text
        print("Debug - Extracted Text:", response_get)
    except (AttributeError, IndexError) as e:
        print(f"Error extracting text: {e}")
        response_get = ""

# Verify the extracted content is a string
    if not isinstance(response_get, str):
        print("Error: Extracted content is not a string.")
        response_get = ""

# Apply regex to extract the skill match score
    score_match = re.search(r"\*\*1\. Skill Match Score:\*\* (\d+)/100", response_get)
    skill_match_score = int(score_match.group(1)) if score_match else None

# Print the extracted score
    print("Skill Match Score:", skill_match_score)

  



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