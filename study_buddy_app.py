import streamlit as st
from transformers import pipeline

# Set up the HuggingFace pipeline (lightweight model for free use)
study_assistant = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", max_new_tokens=256)

# UI Setup
st.set_page_config(page_title="StudyBuddy - Free AI Study Assistant", layout="centered")
st.markdown("<h1 style='text-align: center;'>📘 StudyBuddy - Your Free AI Study Partner</h1>", unsafe_allow_html=True)
st.markdown("### 👋 Hi Student! Ask me anything about your studies below.")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Type your study question here...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking..."):
            try:
                response = study_assistant(f"Student: {user_input}
Assistant:", do_sample=True)[0]["generated_text"]
                assistant_reply = response.split("Assistant:")[-1].strip()
            except Exception as e:
                assistant_reply = f"❌ Error: {e}"

        st.markdown(assistant_reply)
        st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})
