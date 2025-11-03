import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load your dataset
df = pd.read_csv("data/dataset.csv")

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
