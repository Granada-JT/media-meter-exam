from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    """Model representing the response after a file upload.

    Attributes:
        filename (str): The name of the uploaded file.
        message (str): A message indicating the result of the upload.
    """
    filename: str
    message: str
