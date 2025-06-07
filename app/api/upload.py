import os
import uuid

from fastapi import APIRouter, UploadFile

from app.dependencies import SessionDep, SuperAdmin, config
from app.response import UploadedFile


upload = APIRouter(tags=["upload"], prefix="/upload")


@upload.post("/upload")
async def upload_file(file: UploadFile, admin: SuperAdmin):
    file_extension = file.filename.split(".")[-1]
    random_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(config.upload_dir, random_filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return UploadedFile(filename=random_filename)
