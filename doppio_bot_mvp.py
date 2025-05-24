import streamlit as st
from openai import OpenAI

# Set your API key securely
client = OpenAI(api_key="sk-proj-...")  # Replace with your actual key

# Function to get response from OpenAI
def get_answer(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",  # You can also use "gpt-3.5-turbo" or "gpt-4o-mini"
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("Doppio Bot MVP")

user_question = st.text_input("Ask something:")

if user_question:
    answer = get_answer(user_question)
    st.markdown(f"**DoppioBot:** {answer}")
