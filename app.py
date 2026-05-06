
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




import streamlit as st
import google.generativeai as genai
import os

# ---------------------------
# CONFIGURE API KEY
# ---------------------------
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ GOOGLE_API_KEY not found. Add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ---------------------------
# MODEL INITIALIZATION
# ---------------------------
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Gemini AI Chatbot")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chat
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(msg)

# User input
user_input = st.chat_input("Type your message here...")

# ---------------------------
# CHAT LOGIC
# ---------------------------
if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append(("user", user_input))

    try:
        # Generate response
        response = model.generate_content(user_input)

        bot_reply = response.text

    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # Show bot response
    st.chat_message("assistant").write(bot_reply)
    st.session_state.chat_history.append(("assistant", bot_reply))