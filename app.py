import streamlit as st
import time
import requests

# Streamlit UI
st.title("AI Travel Planner Chatbot ✈️")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "trip_details" not in st.session_state:
    st.session_state["trip_details"] = {}
if "current_question" not in st.session_state:
    st.session_state["current_question"] = None
if "greeted" not in st.session_state:
    st.session_state["greeted"] = False
if "waiting_for_reply" not in st.session_state:
    st.session_state["waiting_for_reply"] = False

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

# Function to fetch real-time attractions
def get_real_time_attractions(destination, preferences):
    search_url = f"https://api.example.com/attractions?location={destination}&preferences={preferences}"
    response = requests.get(search_url)
    if response.status_code == 200:
        return response.json().get("attractions", [])
    return ["Explore local attractions", "Visit a recommended site"]

# Function to generate an itinerary
def generate_itinerary():
    details = st.session_state["trip_details"]
    attractions = get_real_time_attractions(details["destination"], details.get("preferences", "general"))
    
    itinerary = f"Here is your {details['days']}-day itinerary for {details['destination']}\n"
    for day in range(1, int(details["days"]) + 1):
        itinerary += f"\n**Day {day}:**\n"
        itinerary += f"- Morning: {attractions[day % len(attractions)]}.\n"
        itinerary += f"- Afternoon: {attractions[(day + 1) % len(attractions)]}.\n"
        itinerary += f"- Evening: {attractions[(day + 2) % len(attractions)]}.\n"
    
    return itinerary

# Greet the user first
if not st.session_state["greeted"]:
    greeting = "Hello! 😊 I'm your AI Travel Assistant. Let's plan your perfect trip! 🌍 Where would you like to go?"
    with st.chat_message("assistant"):
        st.markdown(greeting)
    st.session_state["messages"].append({"role": "assistant", "content": greeting})
    st.session_state["greeted"] = True
    st.session_state["waiting_for_reply"] = True

# Handle user input
user_input = st.chat_input("Tell me about your trip!")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    if st.session_state["waiting_for_reply"]:
        st.session_state["trip_details"]["destination"] = user_input
        st.session_state["current_question"] = "starting_location"
        st.session_state["waiting_for_reply"] = False
    else:
        st.session_state["trip_details"][st.session_state["current_question"]] = user_input
        
        keys = list(questions.keys())
        current_index = keys.index(st.session_state["current_question"])
        if current_index < len(keys) - 1:
            st.session_state["current_question"] = keys[current_index + 1]
        else:
            st.session_state["current_question"] = None
            itinerary = generate_itinerary()
            with st.chat_message("assistant"):
                st.markdown(itinerary)
            st.session_state["messages"].append({"role": "assistant", "content": itinerary})

if st.session_state["current_question"]:
    with st.chat_message("assistant"):
        st.markdown(questions[st.session_state["current_question"]])
