# import streamlit as st
# import google.generativeai as genai
# import os

# # Load Gemini API Key from Streamlit secrets
# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# # Initialize model
# model = genai.GenerativeModel(model_name='models/gemini-pro')

# # Set Up Streamlit UI
# st.set_page_config(page_title="Women in Tech Career Coach", layout="centered")
# st.title("👩‍💻 Women in Tech Career Coach")
# st.markdown("Empowering women to grow in tech careers through personalized guidance.")

# # Build the Chatbot Interface
# with st.form("chat_form"):
#     user_input = st.text_area("💬 Ask me anything about your tech career, resume, courses, or interviews:")
#     submit = st.form_submit_button("Send")

# if submit and user_input:
#     with st.spinner("Thinking..."):
#         response = model.generate_content(user_input)
#         st.markdown(f"**Career Coach:** {response.text}")


import streamlit as st
import google.generativeai as genai

# Load API key securely from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Configure the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.set_page_config(page_title="Women in Tech Career Coach", layout="centered")
st.title("👩‍💻 Women in Tech Career Coach")
st.markdown("Empowering women to grow in tech careers through personalized guidance.")

# Input from user
user_input = st.text_input("💬 Ask me anything about your tech career, resume, courses, or interviews:")

if user_input:
    st.session_state["messages"].append({"role": "user", "parts": user_input})
    try:
        response = model.generate_content(st.session_state["messages"])
        st.session_state["messages"].append({"role": "model", "parts": response.text})
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Display chat history
for msg in st.session_state["messages"]:
    who = "🧑" if msg["role"] == "user" else "🤖"
    st.markdown(f"{who}: **{msg['parts']}**")

# # 📚 Recommend Courses Button
# if st.button("📚 Recommend Courses for Data Science"):
#     course_prompt = "Recommend beginner-friendly Coursera or edX courses for women who want to start a career in Data Science."
#     try:
#         response = model.generate_content(course_prompt)
#         st.markdown(f"🤖: **{response.text}**")
#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")

# # 📄 Resume Review Section
# st.markdown("### 📄 Resume / Cover Letter Review")
# resume_text = st.text_area("Paste your resume or cover letter for feedback:")

# if st.button("🔍 Review My Resume"):
#     resume_prompt = f"Review this resume or cover letter and suggest improvements:\n\n{resume_text}"
#     try:
#         response = model.generate_content(resume_prompt)
#         st.markdown(f"🤖: **{response.text}**")
#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")



