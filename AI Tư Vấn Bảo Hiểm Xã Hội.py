import streamlit as st  
import sys
import os 
from PIL import Image
import base64

# Add background image

st.image("Source/header.png")
st.title("Hệ Thống Tư Vấn Bảo Hiểm Xã Hội Bằng AI")


with st.chat_message("AI"):
    st.markdown("Xin chào! Tôi là AI tư vấn bảo hiểm xã hội của bạn. Tôi có thể giúp gì cho bạn hôm nay?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for item in st.session_state.messages:
    with st.chat_message("AI")
    st.markdown(item)
prompt = st.chat_input("Bạn cần tôi tư vấn gì?")


if prompt:
    with st.chat_message("AI"):
        st.markdown(prompt)
    st.session_state.messages.append(prompt)





# if "messages" not in st.session_state:
#     st.session_state.messages = []

# prompt=st.chat_input("Bạn cần tôi tư vấn gì?")
# with st.chat_message("Me"):
#     st.write(prompt)



# for item in st.session_state.messages:
#     with st.chat_message("AI"):
#         st.markdown(item)
#     st.session_state.messages.append(prompt)