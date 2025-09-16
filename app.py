import os
import dotenv
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load API key
load_dotenv()
st.set_page_config(
    page_title="Chat with Tarun's Bot",
    page_icon="Image.png",
    layout="centered",
)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-2.5-flash')

# ✅ CSS to make only chat area scrollable
st.markdown("""
    <style>
    /* Target the chat container */
    .stChatMessage {
        max-height: 400px;   /* fix height */
        overflow-y: auto;    /* scroll only messages */
    }
    </style>
""", unsafe_allow_html=True)

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Header (static)
col1, col2 = st.columns([6,6])
with col1:
    st.title("BotMate-ChatBot")
with col2:
    st.image("Image.png", width=70)

# Chat history (scrollable now)
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input
user_prompt = st.chat_input("Ask Tarun's bot...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
