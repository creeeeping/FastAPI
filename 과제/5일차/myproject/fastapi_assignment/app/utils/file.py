import os
import uuid
from typing import Union

from fastapi import UploadFile, File, HTTPException

from app.configs import config

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]


async def upload_file(file: Union[File, UploadFile], upload_dir: str) -> str:
    """Save an uploaded file under MEDIA_DIR/upload_dir and return its relative URL.

    - Generates a unique filename using uuid4.
    - Ensures the upload directory exists.
    - Returns a relative path like "users/profile_images/filename.jpg".
    """
    if not getattr(file, "filename", None):
        raise HTTPException(status_code=400, detail="No filename provided.")

    # split filename & extension
    if "." in file.filename:
        filename, ext = file.filename.rsplit(".", 1)
    else:
        filename, ext = file.filename, ""

    # unique filename
    unique_suffix = uuid.uuid4().hex
    if ext:
        unique_filename = f"{filename}_{unique_suffix}.{ext}"
    else:
        unique_filename = f"{filename}_{unique_suffix}"

    # build directory path under MEDIA_DIR
    upload_dir_path = os.path.join(str(config.MEDIA_DIR), upload_dir)
    os.makedirs(upload_dir_path, exist_ok=True)

    # full filesystem path
    full_path = os.path.join(upload_dir_path, unique_filename)

    # save file
    content = await file.read()
    with open(full_path, "wb") as f:
        f.write(content)

    # return relative url (upload_dir/filename)
    return f"{upload_dir}/{unique_filename}"


def delete_file(file_url: str) -> None:
    """Delete a previously saved file if it exists.

    file_url is a relative path like "users/profile_images/xxx.jpg".
    """
    if not file_url:
        return

    full_path = os.path.join(str(config.MEDIA_DIR), file_url)
    if os.path.exists(full_path):
        os.remove(full_path)


def validate_image_extension(file: Union[File, UploadFile]) -> str:
    """Validate that the uploaded file has an allowed image extension.

    Raises HTTPException(400) if invalid.
    Returns the lowercase extension if valid.
    """
    if not getattr(file, "filename", None):
        raise HTTPException(status_code=400, detail="No filename provided.")

    if "." in file.filename:
        _, ext = file.filename.rsplit(".", 1)
    else:
        ext = ""

    ext = ext.lower()
    if ext not in IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"invalid image extension. allowed: {IMAGE_EXTENSIONS}",
        )
    return ext
