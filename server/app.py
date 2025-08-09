from fastapi import FastAPI, UploadFile, File

# Services
from services.ingestion import IngestionService
from services.retrieval import RetrievalService

class RAGServer:
    def __init__(self):
        self.ingestion_service = IngestionService()
        self.retrieval_service = RetrievalService()

rag_server = RAGServer()

app = FastAPI()

app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    return await rag_server.ingestion_service.handle_ingestion(file)
