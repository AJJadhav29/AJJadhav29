import streamlit as st
import google.generativeai as genai
import os

# Load your API key securely
GEMINI_API_KEY = "AIzaSyBJs0nydf5_z39eou2fRm87gZjkXRBOMWs"  # For testing, or use st.secrets in deployment

genai.configure(api_key=GEMINI_API_KEY)

# Create a Gemini model
model = genai.GenerativeModel('gemini-pro')

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



