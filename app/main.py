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
    df = pd.read_csv("data/dataset.csv")
    print("✅ Dataset loaded successfully!")
    print(df.head())

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
