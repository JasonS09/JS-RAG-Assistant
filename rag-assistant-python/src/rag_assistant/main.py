import argparse

from config import Config
from agent import RAGAgent
from fastapi import FastAPI
import uvicorn
from typing import List
from pydantic import BaseModel

# Create FastAPI app instance
app = FastAPI(title="RAG Assistant API")
config = Config()

class AskRequest(BaseModel):
    prompt: str
    document_paths: List[str]= []
    chunk_size: int = 500
    overlap: int = 50
    k: int = 5
    chat_model: str = config.DEFAULT_MODEL
    embeddings_model: str = "nomic-embed-text"

# Add FastAPI routes
@app.post("/ask")
async def ask_question(req: AskRequest):
    prompt = req.prompt
    document_paths = req.document_paths

    rag_agent = RAGAgent(prompt, 
                      document_paths, 
                      req.chunk_size, 
                      req.overlap, 
                      req.k, 
                      req.chat_model, 
                      req.embeddings_model, 
                      config)
    
    # Await the setup
    await rag_agent.setup(config)
    # Use the agent directly since it's returned by setup
    response = rag_agent.chat(prompt)
    print(response)
    return {"response": response}

async def async_main():
    parser = argparse.ArgumentParser(description="RAG assistant CLI: prompt and document paths")
    parser.add_argument(
        "prompt", 
        help="Question or prompt to ask the assistant (wrap in quotes if contains spaces)",
    )
    parser.add_argument(
        "--document-paths",
        nargs="+",
        help="One or more paths to markdown documents to ingest"
    )
    parser.add_argument(
        "--chunk-size",
        default=500,
        type=int,
        help="Size of document chunks to create"
    )
    parser.add_argument(
        "--overlap",
        default=50,
        type=int, 
        help="Number of overlapping characters between chunks"
    )
    parser.add_argument(
        "--k",
        default=5,
        type=int,
        help="Number of top relevant documents to retrieve"
    )
    parser.add_argument(
        "--chat-model",
        default=config.DEFAULT_MODEL,
        help="Chat model to use from Ollama"
    )
    parser.add_argument(
        "--embeddings-model", 
        default="nomic-embed-text",
        help="Embeddings model to use from Ollama"
    )
    args = parser.parse_args()
    rag_agent = RAGAgent(args.prompt, 
                      args.document_paths, 
                      args.chunk_size, 
                      args.overlap, 
                      args.k, 
                      args.chat_model, 
                      args.embeddings_model, 
                      config)
    
    await rag_agent.setup(config)
    response = rag_agent.chat(args.prompt)
    print(response)

if __name__ == "__main__":
    import sys
    import asyncio
    if len(sys.argv) > 1:
        asyncio.run(async_main())
    else:
        # Otherwise run as API server
        uvicorn.run(app, host="0.0.0.0", port=8000)