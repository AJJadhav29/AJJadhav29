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
import fitz  # PyMuPDF
import docx

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

# One-shot Gemini call for fresh prompts (without chat history)
def ask_single_prompt(prompt_text):
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


# # Input from user
# user_input = st.text_input("💬 Ask me anything about your tech career, resume, courses, or interviews:")

# if user_input:
#     st.session_state["last_input"] = user_input
#     st.session_state["messages"].append({"role": "user", "parts": user_input})
#     try:
#         response = model.generate_content(st.session_state["messages"])
#         st.session_state["messages"].append({"role": "model", "parts": response.text})
#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")

# Display chat history
for msg in st.session_state["messages"]:
    who = "🧑" if msg["role"] == "user" else "🤖"
    st.markdown(f"{who}: **{msg['parts']}**")

# Show latest user input again after actions
if "last_input" in st.session_state and not user_input:
    st.markdown(f"🧑: **{st.session_state['last_input']}**")
    
# # Quick Action Buttons
# st.markdown("**Need help with something specific?**")
# col1, col2, col3 = st.columns(3)

# if col1.button("📄 Resume Review"):
#     st.session_state["messages"].append({"role": "user", "parts": "Can you review my resume and give suggestions for improvement?"})

# if col2.button("📚 Suggest Courses"):
#     st.session_state["messages"].append({"role": "user", "parts": "Can you suggest beginner-friendly courses in data science for a woman entering tech?"})

# if col3.button("🎤 Mock Interview"):
#     st.session_state["messages"].append({"role": "user", "parts": "Can you conduct a 3-question mock interview for a frontend developer role?"})


# --- Quick Action Buttons with Direct Gemini Response ---
st.markdown("**Need help with something specific?**")
col1, col2, col3 = st.columns(3)

if col1.button("📄 Resume Review"):
    prompt = "Can you review my resume and give suggestions for improvement?"
    st.markdown(f"🧑: **{prompt}**")
    reply = ask_single_prompt(prompt)
    if reply:
        st.markdown(f"🤖: **{reply}**")

if col2.button("📚 Suggest Courses"):
    prompt = "Can you suggest beginner-friendly courses in data science for a woman entering tech?"
    st.markdown(f"🧑: **{prompt}**")
    reply = ask_single_prompt(prompt)
    if reply:
        st.markdown(f"🤖: **{reply}**")

if col3.button("🎤 Mock Interview"):
    prompt = "Can you conduct a 3-question mock interview for a frontend developer role?"
    st.markdown(f"🧑: **{prompt}**")
    reply = ask_single_prompt(prompt)
    if reply:
        st.markdown(f"🤖: **{reply}**")

# if col1.button("📄 Resume Review"):
#     prompt = "Can you review my resume and give suggestions for improvement?"
#     st.session_state["messages"].append({"role": "user", "parts": prompt})
#     try:
#         response = model.generate_content(st.session_state["messages"])
#         st.session_state["messages"].append({"role": "model", "parts": response.text})
#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")

# if col2.button("📚 Suggest Courses"):
#     prompt = "Can you suggest beginner-friendly courses in data science for a woman entering tech?"
#     st.session_state["messages"].append({"role": "user", "parts": prompt})
#     try:
#         response = model.generate_content(st.session_state["messages"])
#         st.session_state["messages"].append({"role": "model", "parts": response.text})
#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")

# if col3.button("🎤 Mock Interview"):
#     prompt = "Can you conduct a 3-question mock interview for a frontend developer role?"
#     st.session_state["messages"].append({"role": "user", "parts": prompt})
#     try:
#         response = model.generate_content(st.session_state["messages"])
#         st.session_state["messages"].append({"role": "model", "parts": response.text})
#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")

# Resume File Upload
def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        return text

    elif file_type == "docx":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    else:
        return "Unsupported file type."

uploaded_file = st.file_uploader("📎 Upload your resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    extracted_text = extract_text_from_file(uploaded_file)
    prompt = f"Please review my resume and provide feedback:\n{extracted_text}"
    st.markdown(f"🧑: Uploaded resume for review.")
    reply = ask_single_prompt(prompt)
    if reply:
        st.markdown(f"🤖: **{reply}**")

# ----- Multilingual Translation -----
language = st.selectbox("🌐 Respond in:", ["English", "Spanish", "Hindi", "French"])

if language != "English" and st.session_state["messages"]:
    last_response = st.session_state["messages"][-1]["parts"]
    translation_prompt = f"Translate the following text into {language}:\n\n{last_response}"
    translated = ask_single_prompt(translation_prompt)
    if translated:
        st.markdown(f"🌐 **Translated ({language}):** {translated}")

st.markdown("---")
st.subheader("💬 Ask a career-related question")

user_input = st.text_input("Type your question:")

if user_input:
    st.session_state["last_input"] = user_input
    st.session_state["messages"].append({"role": "user", "parts": user_input})
    try:
        response = model.generate_content(st.session_state["messages"])
        st.session_state["messages"].append({"role": "model", "parts": response.text})
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")






















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



