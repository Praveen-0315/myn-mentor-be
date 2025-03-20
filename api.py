from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from catgorize_docs import query_documents, update_document         
import uvicorn

app = FastAPI(title="Document Query API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Query(BaseModel):
    query: str
    top_k: int = 2  # Default value of 2

class QueryResponse(BaseModel):
    relevant_documents: list[str]
    relevant_doc_names: list[str]
    ai_response: str

# Sample curl:
# curl --location 'http://localhost:7158/query' \
# --header 'Content-Type: application/json' \
# --data '{"query": "List all inward assist apis which don'\''t use redis", "top_k": 2}'
@app.post("/query", response_model=QueryResponse)
async def process_query(query_request: Query):
    try:
        results = query_documents(query_request.query, top_k=query_request.top_k)
        
        return QueryResponse(
            relevant_documents=results['relevant_documents'],
            relevant_doc_names=results['relevant_doc_names'],
            ai_response=results['ai_response']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Sample curl:
# curl --location 'http://localhost:7158/update' \
# --header 'Content-Type: application/json'
@app.get("/update")
async def process_query():
    try:
        update_document()
        return {"status" : "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7158) 