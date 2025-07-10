import streamlit as st
import openai
import os

# Use environment variable for OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# App UI
st.set_page_config(page_title="StudyBuddy - AI Study Assistant", layout="centered")
st.markdown("<h1 style='text-align: center;'>📘 StudyBuddy - Your AI Study Partner</h1>", unsafe_allow_html=True)
st.markdown("### 👋 Hi Student! Ask me anything about your studies below.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display message history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your study question here...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        st.markdown("🧠 Thinking...")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a friendly and knowledgeable study assistant for school and college students. Answer simply and clearly."},
                    *st.session_state["messages"]
                ],
                temperature=0.7,
                max_tokens=400
            )
            assistant_reply = response["choices"][0]["message"]["content"]
        except Exception as e:
            assistant_reply = f"❌ Error: {e}"

        st.empty()
        st.markdown(assistant_reply)
        st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})