
import streamlit as st
from datetime import datetime
import re

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="EdgeMind",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------
# SESSION STATE
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------
# CHATBOT RESPONSE ENGINE
# --------------------------------

def chatbot_response(text):

    text = text.lower().strip()
    words = set(re.findall(r"\b[\w']+\b", text))

    if words.intersection({"hello", "hi", "hey"}):
        return "Hello! I am EdgeMind. How can I help you?"

    if "your name" in text:
        return "I am EdgeMind, your offline assistant."

    if "time" in words:
        return "Current time: " + datetime.now().strftime("%H:%M:%S")

    if "date" in words:
        return "Today's date: " + datetime.now().strftime("%d-%m-%Y")

    if "help" in words:
        return (
            "Here are some commands you can try:\n"
            "- Hello\n"
            "- What is your name?\n"
            "- What is the time?\n"
            "- What is the date?\n"
            "- Help\n"
            "- Bye"
        )

    if "bye" in words:
        return "Goodbye! Thank you for using EdgeMind."

    if "thank" in words:
        return "You're welcome! Happy to help."

    return (
        "I don't understand that command yet. "
        "My intelligence is still under development."
    )

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.title("🤖 EdgeMind")

    st.caption("ESP32-S3 Edge AI Project")

    st.divider()

    st.subheader("System Status")

    st.success("Chat interface running")

    st.info("Response engine: Rule-based demo")

    st.warning("ESP32-S3: Not connected")

    st.caption("Hardware communication is not integrated yet.")

    st.divider()

    st.subheader("Chat Controls")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Prototype Version 1.1")

    st.caption("Vishvakarma Awards 2026-27")

# --------------------------------
# MAIN INTERFACE
# --------------------------------

st.title("🤖 EdgeMind")

st.caption("Offline AI Assistant | Prototype v1.1")

st.divider()

# Welcome message

if not st.session_state.messages:

    with st.chat_message("assistant", avatar="🤖"):
        st.write(
            "Hello! I am EdgeMind. "
            "I am your local assistant. How can I help you?"
        )

    st.caption("Try typing 'help' to explore my commands.")

# --------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --------------------------------
# USER INPUT
# --------------------------------

if prompt := st.chat_input("Ask EdgeMind..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    answer = chatbot_response(prompt)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
