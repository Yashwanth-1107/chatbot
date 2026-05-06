import streamlit as st
from groq import Groq

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq AI Chatbot")

# API KEY (STREAMLIT SECRETS)
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# FIXED MODEL (WORKING NOW)
MODEL = "llama-3.3-70b-versatile"

if "chat" not in st.session_state:
    st.session_state.chat = []

for r, m in st.session_state.chat:
    with st.chat_message(r):
        st.write(m)

msg = st.chat_input("Type here...")

if msg:
    st.chat_message("user").write(msg)
    st.session_state.chat.append(("user", msg))

    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are helpful AI"},
                {"role": "user", "content": msg}
            ]
        )

        reply = res.choices[0].message.content

    except Exception as e:
        reply = f"Error: {e}"

    st.chat_message("assistant").write(reply)
    st.session_state.chat.append(("assistant", reply))