from urllib import request
import sys
import os
import uuid
from PIL import Image
import base64
import requests

import streamlit as st
import uuid

# import streamlit as st
# import base64
from pathlib import Path

#Gioi thieu
@st.cache_data
def get_base64_of_bin_file(bin_file: str) -> str:
		with open(bin_file, 'rb') as f:
				data = f.read()
		return base64.b64encode(data).decode()


# --- Page config must be first ---
st.set_page_config(page_title="AI TƯ VẤN BẢO HIỂM XÃ HỘI VIỆT NAM", page_icon=":robot_face:")

# Load images
BG_PATH = Path(r"D:\UIT\AI\LegiSearch\Source\LawAI.jpg")
LOGO_PATH = Path(r"D:\UIT\AI\LegiSearch\Source\BHXHlogo.jpeg")
bg_b64 = get_base64_of_bin_file(BG_PATH)
logo_b64 = get_base64_of_bin_file(LOGO_PATH)

# Custom CSS for background and layout
st.markdown(f"""
<style>
    /* Background image - blurred and centered */
    .stMain {{
        background-image: url("data:image/jpg;base64,{bg_b64}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        overflow: hidden;
    }}
    
    # .stMain::before {{
    #     content: "";
    #     position: fixed;
    #     top: 0;
    #     left: 0;
    #     width: 100%;
    #     height: 100%;
    #     background-color: rgba(255, 255, 255, 0.85);
    #     backdrop-filter: blur(8px);
    #     -webkit-backdrop-filter: blur(8px);
    #     z-index: -1;
    # }}
    
    /* Header with logo and text */
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }}
    
    .header-text {{
        font-size: 1.5rem;
        font-weight: 600;
        color: #0e4d66;
    }}
    
    .header-logo {{
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }}
</style>

<div class="header-container">
    <div class="header-text">Chào mừng đến với AI Tư vấn Bảo Hiểm Xã Hội Việt Nam!</div>
    <img src="data:image/jpeg;base64,{logo_b64}" class="header-logo" />
</div>
""", unsafe_allow_html=True)

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
chat_container = None
# --- Show chat history in scrollable container ---
if not st.session_state.chat_history or len(st.session_state.chat_history) == 0:
    st.warning("Chào bạn! Tôi là trợ lý AI chuyên tư vấn về Bảo hiểm xã hội Việt Nam. Hãy đặt câu hỏi của bạn về các quy định, quyền lợi, thủ tục liên quan đến bảo hiểm xã hội, và tôi sẽ cố gắng giúp bạn!")
else:
    chat_container = st.container(height=400)
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# --- Input ---
prompt = st.chat_input("Vui lòng nhập câu hỏi của bạn về bảo hiểm xã hội.")

if prompt:
    # Add user's message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Generate AI response
    if chat_container is not None:
        with chat_container:
            with st.spinner("Hệ thống đang truy xuất dữ liệu. Vui lòng chờ trong giây lát... ⏳"):
                response = rag_system.generate_answer(prompt, mode="hybrid")
    else:
        with st.spinner("Hệ thống đang truy xuất dữ liệu. Vui lòng chờ trong giây lát... ⏳"):
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
        st.session_state.chat_history.append({"role": "AI", "content": api_response})
    else:
        st.session_state.chat_history.append({"role": "AI", "content": "Error: backend returned no response"})
    
    # Rerun to show the new messages in the container
    st.rerun()