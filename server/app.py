"""RAG Server"""

from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv

from langchain_core.vectorstores import InMemoryVectorStore

# Services
from services.embedding.embedding import EmbeddingService
from services.ingestion.ingestion import IngestionService
from services.retrieval.retrieval import RetrievalService
from services.vector_store.vector_store_manager import VectorStoreManager
from services.llm_service.llm_interface import LLMInterface

load_dotenv()

class RAGServer:
    """RAG Server"""
    def __init__(self):
        self.vector_store_manager: VectorStoreManager = None
        self.vector_store: InMemoryVectorStore = None
        self.embedding_service: EmbeddingService = None
        self.ingestion_service: IngestionService = None
        self.llm_interface: LLMInterface = None
        self.retrieval_service: RetrievalService = None
    
    def initialize_ingestion(self):
        self.vector_store_manager = VectorStoreManager()
        self.vector_store = self.vector_store_manager.vector_store
        self.embedding_service = EmbeddingService(self.vector_store)
        self.ingestion_service = IngestionService(self.embedding_service)
        self.llm_interface = LLMInterface()
        self.retrieval_service = RetrievalService(self.vector_store, self.llm_interface)

rag_server = RAGServer()

app = FastAPI()

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    # Create a new vector store for each ingestion
    rag_server.initialize_ingestion()
    return await rag_server.ingestion_service.handle_ingestion(file)

@app.get("/retrieve")
async def retrieve(query: str):
    return await rag_server.retrieval_service.retrieve(query)