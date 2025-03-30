import streamlit as st
import requests

# Streamlit UI
st.title("AI Travel Planner Chatbot ✈️")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "trip_details" not in st.session_state:
    st.session_state["trip_details"] = {}
if "current_question" not in st.session_state:
    st.session_state["current_question"] = "starting_location"
if "greeted" not in st.session_state:
    st.session_state["greeted"] = False

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Questions to gather details step by step
questions = {
    "starting_location": "Where are you traveling from?",
    "destination": "Where is your destination?",
    "days": "How many days will your trip last?",
    "purpose": "What is the purpose of your trip? (Vacation, Business, etc.)",
    "preferences": "What are your interests? (Adventure, Culture, Relaxation, Food, etc.)",
    "budget": "What is your budget level? (Low, Mid, Luxury)",
    "accommodation": "What type of accommodation do you prefer? (Budget, Mid-range, Luxury)",
    "dietary_preference": "Do you have any dietary preferences? (Vegan, Halal, Gluten-free, etc.)",
    "walking_tolerance": "How comfortable are you with walking long distances? (Low, Moderate, High)"
}

# Function to generate an itinerary
def generate_itinerary():
    details = st.session_state["trip_details"]
    destination = details.get("destination", "your destination")
    days = int(details.get("days", 1))
    preferences = details.get("preferences", "general")
    
    itinerary = f"Here is your {days}-day itinerary for {destination}:\n"
    for day in range(1, days + 1):
        itinerary += f"\n**Day {day}:**\n"
        itinerary += "- Morning: Explore local sights.\n"
        itinerary += "- Afternoon: Visit a recommended attraction.\n"
        itinerary += "- Evening: Try a popular local restaurant.\n"
    
    return itinerary

# Greet the user first
if not st.session_state["greeted"]:
    greeting = "Hello! 😊 I'm your AI Travel Assistant. Let's plan your perfect trip! 🌍"
    with st.chat_message("assistant"):
        st.markdown(greeting)
    st.session_state["messages"].append({"role": "assistant", "content": greeting})
    st.session_state["greeted"] = True

# Ask the first question
if st.session_state["current_question"] == "starting_location":
    first_question = questions["starting_location"]
    with st.chat_message("assistant"):
        st.markdown(first_question)
    st.session_state["messages"].append({"role": "assistant", "content": first_question})

# Handle user input
user_input = st.chat_input("Tell me about your trip!")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    current_q = st.session_state["current_question"]
    if current_q:
        st.session_state["trip_details"][current_q] = user_input
        keys = list(questions.keys())
        current_index = keys.index(current_q)
        
        if current_index < len(keys) - 1:
            st.session_state["current_question"] = keys[current_index + 1]
        else:
            st.session_state["current_question"] = None
            itinerary = generate_itinerary()
            with st.chat_message("assistant"):
                st.markdown(itinerary)
            st.session_state["messages"].append({"role": "assistant", "content": itinerary})
    
# Ask next question
if st.session_state["current_question"]:
    next_question = questions[st.session_state["current_question"]]
    with st.chat_message("assistant"):
        st.markdown(next_question)
    st.session_state["messages"].append({"role": "assistant", "content": next_question})
