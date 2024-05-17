import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://0.0.0.0:8000/brutus/invoke")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        Hi!, I am Brutus, created by Amit and Aayush, I am here to assist you today on your queries, realated to RDK, OneShop Inventory, SLC and some other things.
        Feel free to ask your doubts and questions, but keep in mind I am still under Devlopment :)
        """
    )

    # st.header("Example Questions")
    # st.markdown("- Which hospitals are in the hospital system?")
    # st.markdown("- What is the current wait time at wallace-hamilton hospital?")
    # st.markdown(
    #     "- At which hospitals are patients complaining about billing and "
    #     "insurance issues?"
    # )
    # st.markdown("- What is the average duration in days for closed emergency visits?")
    # st.markdown(
    #     "- What are patients saying about the nursing staff at "
    #     "Castaneda-Hardy?"
    # )
    # st.markdown("- What was the total billing amount charged to each payer for 2023?")
    # st.markdown("- What is the average billing amount for medicaid visits?")
    # st.markdown("- Which physician has the lowest average visit duration in days?")
    # st.markdown("- How much was billed for patient 789's stay?")
    # st.markdown(
    #     "- Which state had the largest percent increase in medicaid visits "
    #     "from 2022 to 2023?"
    # )
    # st.markdown("- What is the average billing amount per day for Aetna patients?")
    # st.markdown("- How many reviews have been written from patients in Florida?")
    # st.markdown(
    #     "- For visits that are not missing chief complaints, "
    #     "what percentage have reviews?"
    # )
    # st.markdown(
    #     "- What is the percentage of visits that have reviews for each hospital?"
    # )
    # st.markdown(
    #     "- Which physician has received the most reviews for this visits "
    #     "they've attended?"
    # )
    # st.markdown("- What is the ID for physician James Cooper?")
    # st.markdown(
    #     "- List every review for visits treated by physician 270. Don't leave any out."
    # )

st.title("Ask Brutus")
st.info(
    "Ask me a question about OneShop Inventory, SLC, RDK and etc."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

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
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
        }
    )