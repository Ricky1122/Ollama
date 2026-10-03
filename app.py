import streamlit as st
import requests 
import json
from memory import ChatMemory


st.set_page_config(page_title="Local AI Chatbot: Bipul ")

OLLAMA_URL = "http://localhost:11434/api/chat"


memory = ChatMemory()

if "messages" not in st.session_state:
    st.session_state.messages = []

def clean_text(text):
    if not text:
        return text

    text = text.replace("\\n", "\n ")
    text = text.replace("\\t", "\t ")
    return text

def stream_response(history):
    payload = {
        "model": "tinyllama",
        "messages": history,
        "stream": True
    }

    with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=(10, 300)) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            decoded_line = line.decode("utf-8")
            data = json.loads(decoded_line)

            if data.get("error"):
                raise RuntimeError(data["error"])
            if data.get("message"):
                yield clean_text(data["message"].get("content", ""))
            if data.get("done"):
                break


st.title("Local AI Chatbot for Healthcare: Developed by Bipul")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Type your message here...Bipul")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):   
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_text = st.write_stream(stream_response(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": response_text})


if st.button("Clear Chat"):
    st.session_state.messages = []
    
            
