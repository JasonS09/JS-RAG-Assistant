import os

class Config:
    """Configuration settings for the RAG assistant application."""
    
    # Database connection settings
    CHROMADB_URL = os.getenv("CHROMADB_URL", "http://localhost:8000")
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    
    # Other settings
    EMBEDDING_DIMENSION = 768  # Example dimension for embeddings
    MAX_DOCUMENTS = 4  # Maximum number of documents to process
    DEFAULT_MODEL = "mistral"