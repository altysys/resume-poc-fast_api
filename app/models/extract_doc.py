import fitz

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()  # Properly close the document
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def process_input(file_path):
    """Process input file and extract text content."""
    try:
        if file_path.endswith('.pdf'):
            return extract_text_from_pdf(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF files are supported.")
    except Exception as e:
        raise Exception(f"Error processing input: {str(e)}")
 
