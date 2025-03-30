import streamlit as st
import time
import subprocess
import sys

# Ensure dependencies are available
def install_and_import(package):
    try:
        __import__(package)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        __import__(package)

install_and_import("streamlit")

# Streamlit UI
st.title("AI Travel Planner")
st.write("Chat with the AI to plan your perfect trip!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Enter your message...")
if user_input:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Simulated AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = f"You said: {user_input}. I'm here to help plan your trip!"
        for chunk in full_response.split():
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Append AI message
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
