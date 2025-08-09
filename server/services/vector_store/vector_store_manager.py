"""Manager for the vector store"""

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

class VectorStoreManager:
    """Manager for the vector store"""
    _vector_store: InMemoryVectorStore = None
    
    def __init__(self):          
        model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )
        self._vector_store = InMemoryVectorStore(model)
    
    @property
    def vector_store(self) -> InMemoryVectorStore:
        return self._vector_store
