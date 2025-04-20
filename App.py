import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from helpers import find_session_by_keyword, format_session_info

load_dotenv()

st.set_page_config(
    page_title="WTM Companion – Event Assistant",
    page_icon="💬",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('models/gemini-pro')

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("💡 WTM Companion")
st.caption("Your AI guide to Women Techmakers IWD 2025 🎉")

# Show history
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

user_input = st.chat_input("Ask me about sessions, speakers, or locations...")
if user_input:
    st.chat_message("user").markdown(user_input)
    gemini_reply = st.session_state.chat_session.send_message(user_input)
    user_question = gemini_reply.text

    # Try to extract session info using Gemini’s understanding
    keyword_guess = gemini_reply.text.strip().split("\n")[0].replace("**", "")
    session = find_session_by_keyword(keyword_guess)
    response = format_session_info(session)

    with st.chat_message("assistant"):
        st.markdown(response)

    # Optional: show map on venue-related queries
    if "where" in user_input.lower() or "location" in user_input.lower():
        st.image("static/venue_map.png", caption="📍 Event Venue Map")
