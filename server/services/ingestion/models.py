from pydantic import BaseModel
from fastapi import UploadFile, File

class IngestionInput(BaseModel):
    file: UploadFile = File(...)