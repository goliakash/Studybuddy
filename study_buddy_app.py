import streamlit as st
from transformers import pipeline
import random

# Load lightweight model from HuggingFace
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

study_assistant = load_model()

# App UI
st.set_page_config(page_title="StudyBuddy - AI Study Assistant", layout="centered")
st.markdown("<h1 style='text-align: center;'>📘 StudyBuddy - Your AI Study Partner</h1>", unsafe_allow_html=True)

# Mode selector
mode = st.radio("Choose Mode", ["📖 Ask a Question", "🎯 Take a Quiz"])

# Subject selector
subject = st.selectbox("Select Subject", ["General", "Math", "Science", "History", "Geography", "Computer Science"])

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Quiz database
quiz_bank = {
    "Math": [
        {"question": "What is 5 + 7?", "answer": "12"},
        {"question": "What is the square root of 81?", "answer": "9"},
    ],
    "Science": [
        {"question": "What planet is known as the Red Planet?", "answer": "Mars"},
        {"question": "What gas do plants absorb?", "answer": "Carbon dioxide"},
    ],
    "History": [
        {"question": "Who was the first President of the USA?", "answer": "George Washington"},
        {"question": "Which country started World War II?", "answer": "Germany"},
    ],
    "Geography": [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "Which ocean is the largest?", "answer": "Pacific"},
    ],
    "Computer Science": [
        {"question": "What does CPU stand for?", "answer": "Central Processing Unit"},
        {"question": "What is the binary number for 5?", "answer": "101"},
    ]
}

# Ask Mode
if mode == "📖 Ask a Question":
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question related to your subject...")

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking..."):
                try:
                    prompt = f"As a {subject} tutor, explain this simply: {user_input}"
                    response = study_assistant(prompt, max_new_tokens=200)[0]["generated_text"]
                    reply = response.strip()
                except Exception as e:
                    reply = f"❌ Error: {e}"

            st.markdown(reply)
            st.session_state["messages"].append({"role": "assistant", "content": reply})

# Quiz Mode
else:
    st.markdown(f"### 🎯 Quiz Time - Subject: {subject}")
    if subject in quiz_bank:
        question = random.choice(quiz_bank[subject])
        user_answer = st.text_input(f"📝 {question['question']}")
        if user_answer:
            if user_answer.strip().lower() == question['answer'].lower():
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer is: {question['answer']}")
    else:
        st.info("No quiz questions available for this subject yet.")
