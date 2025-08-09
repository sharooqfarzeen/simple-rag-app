"""Service for ingesting data into the RAG system"""

from fastapi import UploadFile, File, HTTPException
import asyncio
import logging
import fitz


logger = logging.getLogger(__name__)

class IngestionService:

    async def _validate_file(self, file: UploadFile = File(...)):
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
    async def _extract_text_from_bytes(self, file_bytes: bytes):
        """Extract text from a file bytes"""
        # Extract text
        def _extract():
            pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
            return "/n".join(page.get_text() for page in pdf_doc)
        return await asyncio.to_thread(_extract)

    async def _extract_text(self, file: UploadFile = File(...)):
        """Extract text from a file"""
        # Read file bytes
        file_bytes = await file.read()
        # Extract text
        text = await self._extract_text_from_bytes(file_bytes)
        return text


    async def handle_ingestion(self, file: UploadFile = File(...)):
        """Handle the ingestion of a file into the RAG system"""

        # Validate file
        try:
            await self._validate_file(file)
        except HTTPException as e:
            raise e
        
        # Extract text
        try:
            text = await self._extract_text(file)
        except Exception as e:
            logger.error(f"Error extracting text from file: {e}")
            raise HTTPException(status_code=500, detail="Error extracting text from file")
        
        # Create embeddings
        # Return success
