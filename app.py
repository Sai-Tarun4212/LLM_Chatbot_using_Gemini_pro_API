import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


load_dotenv()
st.set_page_config(
    page_title="Chat with Tarun's Bot",
    page_icon="Tarun1.png",
    layout="centered",
)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_keyY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
col1, col2 = st.columns([6,6])
with col1:
    st.title("Tarun's - ChatBot")
with col2:
    st.image("Tarun1.png", width=70)




for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)
user_prompt = st.chat_input("Ask Tarun's bot...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)