import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# Load OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI()

# Load FAQ data
@st.cache_data
def load_faqs():
    return pd.read_csv("faqs.csv")

df = load_faqs()

# Prompt generator
def generate_prompt(user_question):
    prompt = "You are DoppioBot, a helpful assistant who answers customer questions in German and English. Base your answers on these examples:\n\n"
    for _, row in df.iterrows():
        prompt += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"
    prompt += f"Q: {user_question}\nA:"
    return prompt

# Get answer from OpenAI
def get_answer(user_question):
    prompt = generate_prompt(user_question)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("DoppioBot")
st.write("Ask me a question in German or English.")

user_question = st.text_input("Type your question here:")

if user_question:
    with st.spinner("DoppioBot is thinking..."):
        try:
            answer = get_answer(user_question)
            st.success(answer)
        except Exception as e:
            st.error("Oops! Something went wrong.")
            st.exception(e)
