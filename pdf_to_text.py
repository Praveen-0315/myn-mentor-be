import fitz

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    return text

def extract_text_from_pdfs_in_directory(directory_path):
    """
    Extract text from all PDF files in the given directory.
    Returns a tuple of (texts, filenames).
    """
    import os
    
    texts = []
    filenames = []
    # Iterate through all files in directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            try:
                extracted_text = extract_text_from_pdf(pdf_path)
                texts.append(extracted_text)
                filenames.append(filename)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                
    return texts, filenames

def validate_question(question):
    """
    Validates if the question is relevant to the documentation context using a prompt-based approach
    Returns a tuple of (is_valid, response_message)
    """
    # Define a context-aware prompt template
    prompt_template = """You are a documentation assistant. Your role is to:
    1. Determine if a question is relevant to technical documentation
    2. Only answer questions about the documentation content
    3. Politely redirect off-topic questions
    
    Question: {question}
    
    Is this question related to documentation content? Respond with either:
    - If relevant: "VALID"
    - If off-topic: A polite message explaining that you can only answer questions about the documentation, with 2-3 example relevant questions."""

    # Example response for off-topic questions
    off_topic_response = """I'm designed to help with questions about the documentation content. 
    This question appears to be outside that scope.

    Here are examples of questions I can help with:
    - What are the key features documented in this system?
    - How does the authentication process work?
    - What are the configuration requirements?

    Please feel free to ask any documentation-related questions!"""

    # For now, using a simple keyword check (in practice, you'd use an LLM here)
    off_topic_keywords = ['play', 'song', 'music', 'weather', 'time', 'date',
                         'joke', 'game', 'sports', 'food', 'recipe']
    
    is_off_topic = any(keyword in question.lower() for keyword in off_topic_keywords)
    
    return (not is_off_topic, off_topic_response if is_off_topic else "")

# Example usage
pdf_path = "/Users/bhuvan.dixit/Downloads/Order Indent Service_02095bd8ec324ecbb6d4b88afc2cd1c1-200325-1209-440.pdf" 
extracted_text = extract_text_from_pdf(pdf_path)

# Optionally, save the extracted text to a file for later use
with open('/users/bhuvan.dixit/Downloads/extracted_confluence_text.txt', 'w') as file:
    file.write(extracted_text)

print("Text extraction complete!")