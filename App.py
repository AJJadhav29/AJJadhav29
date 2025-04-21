import streamlit as st
import google.generativeai as genai
import os

# Load Gemini API Key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize model
model = genai.GenerativeModel("gemini-pro")

# Set Up Streamlit UI
st.set_page_config(page_title="Women in Tech Career Coach", layout="centered")
st.title("👩‍💻 Women in Tech Career Coach")
st.markdown("Empowering women to grow in tech careers through personalized guidance.")

# Build the Chatbot Interface
with st.form("chat_form"):
    user_input = st.text_area("💬 Ask me anything about your tech career, resume, courses, or interviews:")
    submit = st.form_submit_button("Send")

if submit and user_input:
    with st.spinner("Thinking..."):
        response = model.generate_content(user_input)
        st.markdown(f"**Career Coach:** {response.text}")



