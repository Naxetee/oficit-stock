from app.db import engine, Base
import app.models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)