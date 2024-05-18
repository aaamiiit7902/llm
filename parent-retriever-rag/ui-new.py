import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://0.0.0.0:8000/brutus/invoke")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        Hi! I am Brutus, created by Amit and Aayush. I'm here to assist you with your queries related to RDK, OneShop Inventory, SLC, and more. 
        Feel free to ask me anything—I'm here to help! Please note, I am still in development, so I might not be perfect yet, but I'm continuously learning and improving. 
        Looking forward to assisting you!
        """
    )
    
st.title("Ask Brutus")
st.info(
    "Ask me a question about OneShop Inventory, SLC, RDK, etc."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["output"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"input": prompt}

    with st.spinner("Please wait ..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""

    st.chat_message("assistant").markdown(output_text)

    # Instead of appending the entire message to the session state, only append the output
    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
        }
    )
