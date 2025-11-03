from agno.agent import Agent, RunOutput
from agno.models.ollama import Ollama
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge.chunking.markdown import MarkdownChunking
from agno.db.json import JsonDb

class RAGAgent:
    def __init__(self, prompt, document_paths, chunk_size, overlap, k, chat_model, embeddings_model, config):
        self.prompt = prompt
        self.document_paths = document_paths
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.k = k
        self.chat_model = chat_model
        self.embeddings_model = embeddings_model
        self.config = config
        self.agent = None  # Will be set by setup

    async def setup(self, config):
        knowledge = None
        
        if self.document_paths:
            knowledge = Knowledge(
                vector_db=ChromaDb(
                    collection="vectors",
                    path="tmp/chromadb",
                    embedder=OllamaEmbedder(id=self.embeddings_model, dimensions=768),
                    persistent_client=True
                ),
                contents_db=JsonDb(db_path="tmp/contents_db.json"),
                max_results=self.k
            )

            # Use add_contents_async directly instead of add_contents
            await knowledge.add_contents_async(
                name="Agentic AI program concepts documents",
                description="Markdown documents showing different concepts about agentic AI programs.",
                paths=self.document_paths, 
                max_documents=config.MAX_DOCUMENTS,
                reader=MarkdownReader(
                    name="Markdown Chunking Reader",
                    chunking_strategy=MarkdownChunking(chunk_size=self.chunk_size, overlap=self.overlap)
                ),
                skip_if_exists=True)

        self.agent = Agent(
            name="Agno Agent",
            model=Ollama(id=self.chat_model),
            knowledge=knowledge,
            instructions=[
                "Search your knowledge base to answer the user's questions as best as you can.",
                "Include source references in your responses when possible."
            ],
            markdown=True,
            debug_level=2
        )
        return self.agent

    def chat(self, prompt):
        if not self.agent:
            raise ValueError("Agent not set up. Call setup() before chat().")
        response: RunOutput = self.agent.run(prompt)
        return response.content