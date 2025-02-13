from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Medalists API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Medalists API is running"}
