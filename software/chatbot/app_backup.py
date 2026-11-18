
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="EdgeMind",
    page_icon="🤖"
)

st.title("🤖 EdgeMind")
st.caption("Offline AI Assistant | Prototype v1.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

def chatbot_response(text):
    text = text.lower()

    if any(word in text for word in ["hello", "hi", "hey"]):
        return "Hello! I am EdgeMind. How can I help you?"

    if "your name" in text:
        return "I am EdgeMind, your offline AI assistant."

    if "time" in text:
        return datetime.now().strftime("%H:%M:%S")

    if "help" in text:
        return "I can understand basic commands. More intelligence is coming!"

    if "bye" in text:
        return "Goodbye! See you again."

    return "I don't understand that yet. I am still learning."

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask EdgeMind..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    answer = chatbot_response(prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()
