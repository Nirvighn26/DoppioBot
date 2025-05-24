import streamlit as st
import pandas as pd
from openai import OpenAI

# Load API key securely from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_data
def load_faqs():
    return pd.read_csv("faqs.csv")

def generate_prompt(user_question):
    prompt = "You are DoppioBot, a helpful AI that answers customer questions in German and English based on the following examples.\n\n"
    for _, row in df.iterrows():
        prompt += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"
    prompt += f"Q: {user_question}\nA:"
    return prompt

def get_answer(user_question):
    prompt = generate_prompt(user_question)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("DoppioBot MVP")
st.write("Ask me anything about your order, our products, or services.")

df = load_faqs()
user_question = st.text_input("
