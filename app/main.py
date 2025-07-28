from fastapi import FastAPI

app = FastAPI(title="Oficit Stock Service")

@app.get("/")
def read_root():
    return {"msg": "Oficit Stock Service is running!"}