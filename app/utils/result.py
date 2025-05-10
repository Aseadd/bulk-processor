import os
from fastapi import UploadFile
from typing import Tuple, Optional
from datetime import datetime
from io import StringIO

LOCAL_STORAGE_PATH = "processed_files"

class LocalFileStorage:
    def __init__(self):
        os.makedirs(LOCAL_STORAGE_PATH, exist_ok=True)

    async def save_file(self, file_id: str, file_content: StringIO) -> str:
        file_path = os.path.join(LOCAL_STORAGE_PATH, file_id)
        with open(file_path, 'w') as f:
            f.write(file_content.getvalue())
        return file_path
    
    def get_download_link(self, file_id: str) -> str:
        return f"/download/{file_id}"
    
    def file_exists(self, file_id: str) -> bool:
        return os.path.exists(os.path.join(LOCAL_STORAGE_PATH, file_id))
    
    async def get_file(self, file_id: str) -> Optional[StringIO]:
        if not self.file_exists(file_id):
            return None
        
        file_path = os.path.join(LOCAL_STORAGE_PATH, file_id)
        with open(file_path, 'r') as f:
            content = StringIO(f.read())
        return content
    

