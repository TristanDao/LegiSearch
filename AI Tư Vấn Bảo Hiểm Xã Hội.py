from urllib import request
import sys
import os
import uuid
from PIL import Image
import base64
import requests

import streamlit as st
import uuid


# --- Page config must be first ---
st.set_page_config(page_title="AI tư vấn bảo hiểm xã hội", page_icon=":robot_face:")

# --- Session initialization ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource
def get_rag_system():
    return LegalRAGSystem()

if "rag_system" not in st.session_state:
    with st.spinner("Initializing AI system, please wait..."):
        from libs.search import LegalRAGSystem
        st.session_state.rag_system = get_rag_system()

rag_system = st.session_state.rag_system
# --- Show chat history ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input ---
prompt = st.chat_input("What's up?")

if prompt:
    # Add user's message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    with st.chat_message("AI"):
        with st.spinner("AI is generating an answer... ⏳"):
            response = rag_system.generate_answer(prompt, mode="hybrid")
            
        # create fake response
        # response = {
        #     "answer": "Đây là câu trả lời giả lập cho câu hỏi của bạn về bảo hiểm xã hội.",
        #     "sources": [
        #         {"title": "Luật Bảo Hiểm Xã Hội 2014", "url": "https://thuvienphapluat.vn/van-ban/lao-dong-ve-lao-dong/luat-bao-hiem-xa-hoi-2014-238201.aspx"},
        #         {"title": "Nghị định 115/2015/NĐ-CP", "url": "https://thuvienphapluat.vn/van-ban/lao-dong-ve-lao-dong/nghi-dinh-115-2015-nd-cp-quy-dinh-ve-bao-hiem-xa-hoi-bao-hiem-y-te-bao-hiem-thue-301828.aspx"}
        #     ]
        # }
        if response is not None:
            api_response = response["answer"]
            st.markdown(api_response)
            st.session_state.chat_history.append({"role": "AI", "content": api_response})
        else:
            st.error("Error: backend returned no response")