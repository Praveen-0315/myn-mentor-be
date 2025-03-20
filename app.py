import streamlit as st
from catgorize_docs import query_documents
import time
import os

# Configure environment for torch/faiss compatibility
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

def init_session_state():
    if 'history' not in st.session_state:
        st.session_state.history = []

def main():
    try:
        # Set page title and configuration
        st.set_page_config(page_title="Document Query Assistant", layout="wide")
        
        # Add header
        st.title("Document Query Assistant")
        
        # Add text input for query
        user_query = st.text_area("Enter your query:", height=100)
        
        # Add sidebar with options
        with st.sidebar:
            st.subheader("Settings")
            top_k = st.slider("Number of relevant documents", 1, 5, 2)
        
        # Submit button section
        if st.button("Submit"):
            if user_query:
                with st.spinner("Processing your query..."):
                    try:
                        results = query_documents(user_query, top_k=top_k)
                        print('results are:', results)
                        
                        # Display results in two columns
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Relevant Documents")
                            for i, doc in enumerate(results['relevant_documents'], 1):
                                st.write(f"Document {i}")
                                st.write(f"Document Name: {results['relevant_doc_names'][i-1]}")
                        with col2:
                            st.subheader("AI Response")
                            st.markdown(results['ai_response'])
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a query.")

        # Add footer
        st.markdown("---")
        st.markdown("Built with Streamlit")

    except Exception as e:
        st.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main() 