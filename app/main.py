from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.familia import Familia

app = FastAPI(title="Oficit Stock Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"msg": "Oficit Stock Service is running!"}


@app.get("/familias")
def listar_familias(db: Session = Depends(get_db)):
    return db.query(Familia).all()