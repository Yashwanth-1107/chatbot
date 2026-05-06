
# import streamlit as st
# import google.generativeai as genai

# genai.configure(api_key="Gemini_API_KEY ")

# model = genai.GenerativeModel("gemini-2.5-flash")

# st.title("💬 AI Chatbot (ChatGPT Style)")

# # 🔥 memory
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 🔥 show chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])

# # 🔥 input box (like ChatGPT)
# user_input = st.chat_input("Type your message...")

# if user_input:
#     # user message
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     with st.chat_message("user"):
#         st.write(user_input)

#     # AI response
#     response = model.generate_content(user_input)
#     bot_reply = response.text

#     st.session_state.messages.append({"role": "assistant", "content": bot_reply})

#     with st.chat_message("assistant"):
#         st.write(bot_reply)




# import streamlit as st
# import google.generativeai as genai
# import os

# # ---------------------------
# # CONFIGURE API KEY
# # ---------------------------
# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     st.error("⚠️ GOOGLE_API_KEY not found. Add it in Streamlit Secrets.")
#     st.stop()

# genai.configure(api_key=api_key)

# # ---------------------------
# # MODEL INITIALIZATION
# # ---------------------------
# model = genai.GenerativeModel("gemini-pro")

# # ---------------------------
# # STREAMLIT UI
# # ---------------------------
# st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
# st.title("🤖 Gemini AI Chatbot")

# # Chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Display previous chat
# for role, msg in st.session_state.chat_history:
#     with st.chat_message(role):
#         st.write(msg)

# # User input
# user_input = st.chat_input("Type your message here...")

# # ---------------------------
# # CHAT LOGIC
# # ---------------------------
# if user_input:
#     # Show user message
#     st.chat_message("user").write(user_input)
#     st.session_state.chat_history.append(("user", user_input))

#     try:
#         # Generate response
#         response = model.generate_content(user_input)

#         bot_reply = response.text

#     except Exception as e:
#         bot_reply = f"⚠️ Error: {str(e)}"

#     # Show bot response
#     st.chat_message("assistant").write(bot_reply)
#     st.session_state.chat_history.append(("assistant", bot_reply))


import streamlit as st
from groq import Groq

# ---------------------------
# STREAMLIT CONFIG
# ---------------------------
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")

st.title("🤖 Groq AI Chatbot")

# ---------------------------
# API KEY (STREAMLIT SECRETS)
# ---------------------------
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("⚠️ GROQ_API_KEY not found in Streamlit Secrets")
    st.stop()

client = Groq(api_key=api_key)

# ---------------------------
# GET BEST AVAILABLE MODEL (SAFE)
# ---------------------------
def get_best_model():
    try:
        models = client.models.list()
        model_ids = [m.id for m in models.data]

        preferred_models = [
            "llama-3.3-70b-versatile",
            "llama-3.3-8b-instant",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]

        for m in preferred_models:
            if m in model_ids:
                return m

        return model_ids[0]

    except Exception:
        return "llama-3.3-70b-versatile"

MODEL = get_best_model()

st.caption(f"Using model: {MODEL}")

# ---------------------------
# SESSION STATE (CHAT MEMORY)
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(msg)

# ---------------------------
# USER INPUT
# ---------------------------
user_input = st.chat_input("Type your message...")

# ---------------------------
# CHAT LOGIC
# ---------------------------
if user_input:
    # show user message
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append(("user", user_input))

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # show bot reply
    st.chat_message("assistant").write(bot_reply)
    st.session_state.chat_history.append(("assistant", bot_reply))