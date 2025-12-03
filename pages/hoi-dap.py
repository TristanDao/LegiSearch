import streamlit as st
import base64
from PIL import Image
import sys
import os

def add_bg_from_local(image_file):
    with open (image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode() 
        css = f"""
        <style>
        stApp{{
            background-image:url(data:image/png; base64; {encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment:fixed;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
add_bg_from_local(("D:\\UIT\\AI\\LegiSearch\\Source\\AI-Law.jpeg"))
st.title("Hỏi Đáp AI")

prompt=st.chat_input("Bạn cần tôi tư vấn gì?")
