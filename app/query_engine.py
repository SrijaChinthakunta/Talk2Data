import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load your dataset with proper path handling
import os
from pathlib import Path

# Try multiple possible paths for the dataset
possible_paths = [
    "data/dataset.csv",  # Relative to current working directory
    "../data/dataset.csv",  # Relative to project root
    os.path.join(os.path.dirname(__file__), "../data/dataset.csv"),  # Absolute path from app directory
    "./data/dataset.csv"  # Current directory
]

df = None
for path in possible_paths:
    try:
        path = os.path.normpath(path)  # Normalize the path
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"✅ Dataset loaded successfully in query_engine from: {path}")
            break
    except Exception as e:
        print(f"Failed to load from {path}: {e}")
        continue

if df is None:
    raise FileNotFoundError("Could not find dataset.csv in any expected location")

def ask_data(question: str):
    """Answer natural language questions about the dataset"""
    # Convert dataframe to string for AI context
    context = df.to_string(index=False)[:4000]  # keep small for token limit
    prompt = f"""
You are a data assistant. Use the following dataset to answer the question accurately.

DATASET:
{context}

QUESTION:
{question}

Answer only using information from the dataset.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
