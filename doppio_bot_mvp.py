import streamlit as st import openai from langdetect import detect import pandas as pd

Set your OpenAI API Key

openai.api_key = "YOUR_OPENAI_API_KEY"

Load FAQs for different business types (sample CSV: 'business_type,question,answer')

def load_faqs(business_type): try: df = pd.read_csv("faqs.csv") return df[df["business_type"] == business_type] except: return pd.DataFrame(columns=["question", "answer"])

Language detection

def detect_language(text): try: return detect(text)  # 'de' or 'en' except: return 'en'

Generate response with GPT

def generate_gpt_response(user_input, language, business_type): prompt = f""" You are a polite and helpful AI customer support assistant for a small {business_type} business in Germany. The user message is in {language}. Answer in the same language, using a clear and friendly tone. Here is the customer question: {user_input} """

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
except Exception as e:
    return "Sorry, I'm having trouble responding right now."

App layout

st.set_page_config(page_title="DoppioBot - Bilingual AI Assistant") st.title("DoppioBot - Your Bilingual AI Assistant")

business_type = st.selectbox("Select your business type:", ["real_estate", "doctor", "ecommerce"]) user_input = st.text_input("Ask your question in German or English:")

if user_input: lang = detect_language(user_input) lang_text = "German" if lang == "de" else "English" faqs = load_faqs(business_type)

# Check FAQ match
faq_match = faqs[faqs["question"].str.contains(user_input, case=False, na=False)]
if not faq_match.empty:
    answer = faq_match.iloc[0]["answer"]
    st.markdown(f"**({lang_text}) FAQ Answer:** {answer}")
else:
    gpt_response = generate_gpt_response(user_input, lang_text, business_type)
    st.markdown(f"**({lang_text}) AI Answer:** {gpt_response}")
