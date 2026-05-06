import streamlit as st
from groq import Groq

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")

st.title("🤖 Groq AI Chatbot")

# ---------------------------
# API KEY (Streamlit Secrets)
# ---------------------------
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# ---------------------------
# SAFE MODEL (DO NOT CHANGE OLD MODELS)
# ---------------------------
MODEL = "llama-3.1-8b-instant"

# ---------------------------
# SESSION STATE (CHAT MEMORY)
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------------------
# USER INPUT
# ---------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # GROQ API CALL
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                *st.session_state.messages
            ]
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        bot_reply = f"⚠️ Error: {e}"

    # show bot reply
    st.chat_message("assistant").write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})