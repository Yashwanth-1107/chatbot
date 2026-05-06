
import streamlit as st
import google.generativeai as genai

genai.configure(api_key="Gemini_API_KEY ")

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("💬 AI Chatbot (ChatGPT Style)")

# 🔥 memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔥 show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 🔥 input box (like ChatGPT)
user_input = st.chat_input("Type your message...")

if user_input:
    # user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # AI response
    response = model.generate_content(user_input)
    bot_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.write(bot_reply)