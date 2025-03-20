import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from collections import defaultdict
from pdf_to_text import extract_text_from_pdfs_in_directory
import requests
import json

global documents, doc_names  # Need to declare as global first
documents, doc_names = extract_text_from_pdfs_in_directory("/Users/bhuvan.dixit/Documents/Docs/OI")

# Initialize models
keyword_model = KeyBERT()
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract Keywords
document_keywords = {}
for i, doc in enumerate(documents):
    keywords = keyword_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words='english')
    document_keywords[i] = [kw[0] for kw in keywords]

# Generate Embeddings
document_embeddings = embedding_model.encode(documents, normalize_embeddings=True)
dim = document_embeddings.shape[1] 

# Indexing using FAISS
index = faiss.IndexFlatL2(dim)
index.add(np.array(document_embeddings))

# Categorizing Documents by Keywords
document_category_map = defaultdict(list)
for i, keywords in document_keywords.items():
    for kw in keywords:
        document_category_map[kw].append(i)


def query_documents(query, top_k=2):
    # Get relevant documents
    query_embedding = embedding_model.encode([query], normalize_embeddings=True)
    _, top_indices = index.search(np.array(query_embedding), top_k)
    
    query_keywords = [kw[0] for kw in keyword_model.extract_keywords(query, keyphrase_ngram_range=(1, 2), stop_words='english')]
    keyword_matched_docs = set()
    
    for kw in query_keywords:
        if kw in document_category_map:
            keyword_matched_docs.update(document_category_map[kw])
    
    result_docs = set(top_indices[0]).union(keyword_matched_docs)
    
    relevant_docs = []
    relevant_doc_names = []
    for i in result_docs:
        relevant_docs.append(documents[i])
        relevant_doc_names.append(doc_names[i])
    print("relevant_docs are:", relevant_docs)
    print("relevant_doc_names are:", relevant_doc_names)
    
    # Send query to GPT API
    url = "https://genvoy.flipkart.net/gpt-4o-mini/chat/completions?api-version=2023-09-15-preview"
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": "4b94d2e1e3114f358f785bba6685f51b"
    }
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": "Generate a summary of the following query: " + query + " \n\n based on data in these relevant documents: " + "\n\n".join(relevant_docs)
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.7,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "top_p": 0.95,
        "stop": None
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        print('payload is:', payload)
        print('response is:', response_json)
        ai_response = response_json['choices'][0]['message']['content']
        return {
            'relevant_documents': relevant_docs,
            'relevant_doc_names': relevant_doc_names,
            'ai_response': ai_response
        }
    except requests.exceptions.RequestException as e:
        return {
            'relevant_documents': relevant_docs,
            'relevant_doc_names': relevant_doc_names,
            'ai_response': f"Error calling AI API: {str(e)}"
        }
    
def update_document():
    global documents, doc_names  
    documents, doc_names = extract_text_from_pdfs_in_directory("/Users/bhuvan.dixit/Documents/Docs/OI")
    print(len(documents))
    print("Model updated!")


if __name__ == "__main__":
    while True:
        user_query = input("Enter your query (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
            
        results = query_documents(user_query)
        print("\nRelevant Documents:")
        for i, doc in enumerate(results['relevant_documents'], 1):
            print(f"\nDocument {i}:")
            print(doc[:200] + "..." if len(doc) > 200 else doc)
            
        print("\nAI Response:")
        print(results['ai_response'])