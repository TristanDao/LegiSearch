from urllib import request
import streamlit as st  
import sys
import os 
from PIL import Image
import base64

import requests 

def clear_session_state():
    for key in st.session_state.key():
        del st.session_state[key]

import uuid 
#Generate a random session id
# session_id = str(uuid.uuid4())

if session_id not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "flask_api_url" not in st.session_state:
    st.session_state.flask_api_url = None

#Function to display the dialog and set the URL
@st.dialog("Setup Back end")
def vote():
    clear_session_state()
    st.markdown(
        """
        Run the backend here:
        """
    )
    link = st.text_input("Backend URL", "")
    if st.button("Save"):
        st.session_state.flask_api_url ="{}/chat".format_map(link)
        st.success("Backend URL saved!")
        st.rerun()

#Display the dialog only if the URL is not set
if st.session_state.flask_api_url is None:
    vote()

#Onve the URL is set, display it or proceed with the other

if "flask_api_url" in st.session.state:
    st.write("Backend is set to: ", st.session_state.flask_api_url)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#URL of the Flask API

#Display the chat history using chat UI

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    #Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    #Display user message in chat message container:
    with st.chat_message("user"):
        st.markdown(prompt)
#Display assistant response in chat message container
#Prepare the payload for the request

    with st.chat_message("AI"):
        session_id = st.session_state.session_id
        print('--session id',session_id)
        payload = {
            "message":{"content":prompt},
            "sessionID":session_id
    }
    #Send the POST request to the Flask API
        response = requests.post(st.session_state.flask_api_url, json=payload)
    # Check  if the request was successful  
        if response.status_code == 200:
            #Get the response from API
            api_response = response.json()
            #Add the assistant's response to the chat
            st.markdown(api_response["content"])
            st.session_state.chat_history.append({"role": "AI", "content": api_response["content"]})
        else:
            st.error(f"Error:{response.status_code}")


# Add background image

# st.image("Source/header.png")
# st.title("Hệ Thống Tư Vấn Bảo Hiểm Xã Hội Bằng AI")


# with st.chat_message("AI"):
#     st.markdown("Xin chào! Tôi là AI tư vấn bảo hiểm xã hội của bạn. Tôi có thể giúp gì cho bạn hôm nay?")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for item in st.session_state.messages:
#     with st.chat_message("AI")
#     st.markdown(item)
# prompt = st.chat_input("Bạn cần tôi tư vấn gì?")


# if prompt:
#     with st.chat_message("AI"):
#         st.markdown(prompt)
#     st.session_state.messages.append(prompt)





# if "messages" not in st.session_state:
#     st.session_state.messages = []

# prompt=st.chat_input("Bạn cần tôi tư vấn gì?")
# with st.chat_message("Me"):
#     st.write(prompt)



# for item in st.session_state.messages:
#     with st.chat_message("AI"):
#         st.markdown(item)
#     st.session_state.messages.append(prompt)