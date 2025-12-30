from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from app.query_engine import ask_data


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to specific origins like ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load dataset when app starts
@app.on_event("startup")
def load_data():
    global df
    import os
    from pathlib import Path
    
    # Try multiple possible paths for the dataset
    possible_paths = [
        "data/dataset.csv",  # Relative to current working directory
        "../data/dataset.csv",  # Relative to project root
        os.path.join(os.path.dirname(__file__), "../data/dataset.csv"),  # Absolute path from app directory
        "./data/dataset.csv"  # Current directory
    ]
    
    for path in possible_paths:
        try:
            path = os.path.normpath(path)  # Normalize the path
            if os.path.exists(path):
                df = pd.read_csv(path)
                print(f"✅ Dataset loaded successfully from: {path}")
                print(df.head())
                return
        except Exception as e:
            print(f"Failed to load from {path}: {e}")
            continue
    
    # If no path worked, raise an error
    raise FileNotFoundError("Could not find dataset.csv in any expected location")

@app.get("/")
def home():
    return {"message": "Talk2Data API is running!"}

@app.get("/data")
def get_data():
    return df.head(5).to_dict(orient="records")


class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    answer = ask_data(request.question)
    return {"question": request.question, "answer": answer}
