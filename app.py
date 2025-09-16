import os
import dotenv
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-2.5-flash')

# Page config
st.set_page_config(
    page_title="Tarun's AI ChatBot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-container {
        max-width: 700px;
        margin: auto;
        background: white;
        padding: 25px 30px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px 15px;
        margin: 8px 0;
    }
    .stChatMessage[data-testid="stChatMessage-user"] {
        background-color: #DCF8C6;
        text-align: right;
    }
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background-color: #F1F1F1;
        border: 1px solid #EAEAEA;
    }
    </style>
""", unsafe_allow_html=True)

# Chat session
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Centered container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Header
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("🤖 AI ChatBot")
        st.markdown("Talk with a Gemini-powered assistant ✨ ")
    with col2:
        st.image("Image.png", width=70)

    st.markdown("---")

    # Chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # User input
    user_prompt = st.chat_input("Type your message here...")
    if user_prompt:
        with st.chat_message("user"):
            st.markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

    st.markdown('</div>', unsafe_allow_html=True)
