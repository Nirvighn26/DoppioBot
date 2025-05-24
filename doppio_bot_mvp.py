import streamlit as st
import pandas as pd
import openai
from langdetect import detect

st.set_page_config(page_title="DoppioBot", layout="centered")

st.title("DoppioBot - German AI Assistant")
st.markdown("Ask me anything related to your business or product FAQs!")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load FAQs
@st.cache_data
def load_faqs():
    df = pd.read_csv("faqs.csv")
    return df

faqs = load_faqs()

def generate_prompt(user_question):
    prompt = "You are a helpful AI assistant for a German business. Answer the user's question based only on the following FAQs:\n\n"
    for index, row in faqs.iterrows():
        prompt += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"
    prompt += f"\nUser question: {user_question}\nAnswer:"
    return prompt

def get_answer(user_question):
    prompt = generate_prompt(user_question)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a helpful AI assistant for German FAQs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# User input
user_question = st.text_input("Type your question here:")

if user_question:
    st.write("Generating answer...")
    answer = get_answer(user_question)
    st.markdown(f"**Answer:** {answer}")
