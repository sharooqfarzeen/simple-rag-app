"""Service for embedding text"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

class EmbeddingService:
    def __init__(self, vector_store: InMemoryVectorStore):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=100
        )
    
    async def embed_and_store(self, text: str, metadata: dict = None) -> dict:
        """Embed and store text in the vector store"""
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        # Create documents
        documents = [
            Document(page_content=chunk, metadata=metadata or {})
            for chunk in chunks
        ]
        # Add documents to vector store
        ids = self.vector_store.add_documents(documents)
        return {"chunks_created": len(chunks), "document_ids": ids}