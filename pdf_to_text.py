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


# Example usage
pdf_path = "/Users/bhuvan.dixit/Downloads/Order Indent Service_02095bd8ec324ecbb6d4b88afc2cd1c1-200325-1209-440.pdf" 
extracted_text = extract_text_from_pdf(pdf_path)

# Optionally, save the extracted text to a file for later use
with open('/users/bhuvan.dixit/Downloads/extracted_confluence_text.txt', 'w') as file:
    file.write(extracted_text)

print("Text extraction complete!")