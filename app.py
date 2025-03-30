import streamlit as st
import time
import re
from datetime import datetime
import requests

# Streamlit UI
st.title("AI Travel Planner")
st.write("Chat with the AI to plan your perfect trip!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "trip_details" not in st.session_state:
    st.session_state["trip_details"] = {}
if "current_question" not in st.session_state:
    st.session_state["current_question"] = "starting_location"

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Questions to gather details step by step
questions = {
    "starting_location": "Where are you traveling from?",
    "destination": "Where is your destination?",
    "days": "How many days will your trip last?",
    "preferences": "What are your preferences for activities (e.g., adventure, culture, relaxation)?",
    "budget": "What is your budget level? (low, mid, luxury)",
    "accessibility": "Do you have any accessibility requirements?",
    "accommodation": "What type of accommodation do you prefer? (budget, mid-range, luxury)",
    "travel_dates": "What are your travel dates? (e.g., 10/05/2025 to 15/05/2025)",
    "dietary_preference": "Do you have any dietary preferences? (vegan, halal, gluten-free, etc.)"
}

# Function to fetch real-time attractions
def get_real_time_attractions(destination):
    search_url = f"https://api.example.com/attractions?location={destination}"
    response = requests.get(search_url)
    if response.status_code == 200:
        return response.json().get("attractions", [])
    return ["Explore local attractions", "Visit a recommended site"]

# Function to fetch estimated costs
def get_estimated_costs(budget, days):
    cost_per_day = {"low": 50, "mid": 150, "luxury": 400}
    return cost_per_day.get(budget, 150) * days

# Function to fetch real-time flight and hotel costs
def get_real_time_flight_hotel_costs(starting_location, destination, travel_dates):
    flight_search_url = f"https://api.example.com/flights?from={starting_location}&to={destination}&dates={travel_dates}"
    hotel_search_url = f"https://api.example.com/hotels?location={destination}&dates={travel_dates}"
    
    flight_response = requests.get(flight_search_url)
    hotel_response = requests.get(hotel_search_url)
    
    flight_cost = flight_response.json().get("average_price", "Not available") if flight_response.status_code == 200 else "Not available"
    hotel_cost = hotel_response.json().get("average_price_per_night", "Not available") if hotel_response.status_code == 200 else "Not available"
    
    return flight_cost, hotel_cost

# Function to generate an itinerary
def generate_itinerary():
    details = st.session_state["trip_details"]
    estimated_cost = get_estimated_costs(details["budget"], details["days"])
    flight_cost, hotel_cost = get_real_time_flight_hotel_costs(details["starting_location"], details["destination"], details["travel_dates"])
    
    itinerary = f"Here is your {details['days']}-day itinerary for {details['destination']} (Starting from {details['starting_location']}, Travel Dates: {details['travel_dates']}):\n"
    itinerary += f"\nEstimated Budget: ${estimated_cost}\n"
    itinerary += f"Flight Cost: ${flight_cost}\n"
    itinerary += f"Hotel Cost per Night: ${hotel_cost}\n"
    itinerary += f"Dietary Preference: {details['dietary_preference']}\n"
    
    attractions = get_real_time_attractions(details["destination"])
    
    for day in range(1, details["days"] + 1):
        itinerary += f"\n**Day {day}:**\n"
        itinerary += f"- Morning: {attractions[day % len(attractions)]}.\n"
        itinerary += f"- Afternoon: {attractions[(day + 1) % len(attractions)]}.\n"
        itinerary += f"- Evening: {attractions[(day + 2) % len(attractions)]}.\n"
    
    return itinerary

# Collect user input step by step
if st.session_state["current_question"]:
    user_input = st.chat_input(questions[st.session_state["current_question"]])
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Store user response
        st.session_state["trip_details"][st.session_state["current_question"]] = user_input
        
        # Move to the next question
        keys = list(questions.keys())
        current_index = keys.index(st.session_state["current_question"])
        if current_index < len(keys) - 1:
            st.session_state["current_question"] = keys[current_index + 1]
        else:
            st.session_state["current_question"] = None
            itinerary = generate_itinerary()
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_text = ""
                for chunk in itinerary.split():
                    time.sleep(0.05)
                    full_text += chunk + " "
                    message_placeholder.markdown(full_text + "▌")
                message_placeholder.markdown(full_text.strip())
            st.session_state["messages"].append({"role": "assistant", "content": itinerary})
