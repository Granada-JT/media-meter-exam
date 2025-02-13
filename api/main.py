from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Medalists API")

app.include_router(router)

@app.get("/")
def root():
    """Root endpoint to verify that the API is running.

    Returns:
        dict: A message indicating the API status.
    """
    return {"message": "Medalists API is running"}
