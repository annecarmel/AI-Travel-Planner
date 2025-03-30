import streamlit as st
import time
import re
from datetime import datetime

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

# Function to refine user input
def extract_trip_details(user_input):
    match = re.search(r'Trip to ([A-Za-z ]+) for (\d+) days,? (.+)', user_input, re.IGNORECASE)
    if match:
        destination = match.group(1).strip()
        days = int(match.group(2).strip())
        preferences = match.group(3).strip()
        return destination, days, preferences
    return None, None, None

# Function to generate an itinerary
def generate_itinerary(destination, days, preferences):
    itinerary = f"Here is your {days}-day itinerary for {destination}:\n"
    
    activities = {
        "history": ["Visit historical landmarks", "Explore a museum", "Take a guided history tour"],
        "food": ["Try local street food", "Dine at a famous restaurant", "Take a cooking class"],
        "adventure": ["Go hiking in scenic areas", "Try water sports", "Experience a jungle safari"],
        "beach": ["Relax on a famous beach", "Enjoy a boat tour", "Try snorkeling or diving"],
        "culture": ["Watch a traditional performance", "Visit local markets", "Explore an art gallery"],
        "hidden gems": ["Discover lesser-known spots", "Visit unique local attractions", "Explore secret viewpoints"]
    }
    
    user_preferences = preferences.lower().split(" and ")
    
    for day in range(1, days + 1):
        itinerary += f"\n**Day {day}:**\n"
        itinerary += f"- Morning: {activities.get(user_preferences[0], ['Explore a top attraction'])[day % len(activities.get(user_preferences[0], ['Explore a top attraction']))]}.\n"
        itinerary += f"- Afternoon: {activities.get(user_preferences[1] if len(user_preferences) > 1 else 'food', ['Try local cuisine'])[day % len(activities.get(user_preferences[1] if len(user_preferences) > 1 else 'food', ['Try local cuisine']))]}.\n"
        itinerary += f"- Evening: {activities.get(user_preferences[2] if len(user_preferences) > 2 else 'culture', ['Enjoy a cultural event'])[day % len(activities.get(user_preferences[2] if len(user_preferences) > 2 else 'culture', ['Enjoy a cultural event']))]}.\n"
    return itinerary

# User Input
user_input = st.chat_input("Enter your travel details (e.g., 'Trip to Paris for 5 days, loves history and food')...")
if user_input:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Extract trip details
    destination, days, preferences = extract_trip_details(user_input)
    if destination and days and preferences:
        itinerary = generate_itinerary(destination, days, preferences)
    else:
        itinerary = "Could you provide more details? (e.g., 'Trip to Tokyo for 3 days, loves anime and food')"
    
    # AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_text = ""
        for chunk in itinerary.split():
            time.sleep(0.05)
            full_text += chunk + " "
            message_placeholder.markdown(full_text + "▌")
        message_placeholder.markdown(full_text.strip())
    
    # Append AI message
    st.session_state["messages"].append({"role": "assistant", "content": itinerary})
