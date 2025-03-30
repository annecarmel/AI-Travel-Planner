import streamlit as st
import time
import re
from datetime import datetime
import requests

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
    match = re.search(r'Trip from ([A-Za-z ]+) to ([A-Za-z ]+) for (\d+) days,? (.+)', user_input, re.IGNORECASE)
    if match:
        starting_location = match.group(1).strip()
        destination = match.group(2).strip()
        days = int(match.group(3).strip())
        preferences = match.group(4).strip()
        return starting_location, destination, days, preferences
    return None, None, None, None

# Function to refine additional trip details
def extract_additional_details(user_input):
    budget_match = re.search(r'budget: ([A-Za-z]+)', user_input, re.IGNORECASE)
    accessibility_match = re.search(r'accessibility: ([A-Za-z]+)', user_input, re.IGNORECASE)
    accommodation_match = re.search(r'accommodation: ([A-Za-z]+)', user_input, re.IGNORECASE)
    travel_dates_match = re.search(r'travel dates: ([\d-/]+ to [\d-/]+)', user_input, re.IGNORECASE)
    dietary_match = re.search(r'diet: ([A-Za-z]+)', user_input, re.IGNORECASE)
    
    budget = budget_match.group(1).strip() if budget_match else "mid"
    accessibility = accessibility_match.group(1).strip() if accessibility_match else "standard"
    accommodation = accommodation_match.group(1).strip() if accommodation_match else "mid-range"
    travel_dates = travel_dates_match.group(1).strip() if travel_dates_match else "Not specified"
    dietary_preference = dietary_match.group(1).strip() if dietary_match else "No preference"
    
    return budget, accessibility, accommodation, travel_dates, dietary_preference

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
def generate_itinerary(starting_location, destination, days, preferences, budget, accessibility, accommodation, travel_dates, dietary_preference):
    estimated_cost = get_estimated_costs(budget, days)
    flight_cost, hotel_cost = get_real_time_flight_hotel_costs(starting_location, destination, travel_dates)
    
    itinerary = f"Here is your {days}-day itinerary for {destination} (Starting from {starting_location}, Travel Dates: {travel_dates}):\n"
    itinerary += f"\nEstimated Budget: ${estimated_cost}\n"
    itinerary += f"Flight Cost: ${flight_cost}\n"
    itinerary += f"Hotel Cost per Night: ${hotel_cost}\n"
    itinerary += f"Dietary Preference: {dietary_preference}\n"
    
    attractions = get_real_time_attractions(destination)
    
    for day in range(1, days + 1):
        itinerary += f"\n**Day {day}:**\n"
        itinerary += f"- Morning: {attractions[day % len(attractions)]}.\n"
        itinerary += f"- Afternoon: {attractions[(day + 1) % len(attractions)]}.\n"
        itinerary += f"- Evening: {attractions[(day + 2) % len(attractions)]}.\n"
    
    return itinerary

# User Input
user_input = st.chat_input("Enter your travel details (e.g., 'Trip from New York to Paris for 5 days, loves history and food. Budget: mid, Accessibility: standard, Accommodation: luxury, Travel Dates: 10/05/2025 to 15/05/2025, Diet: vegan')...")
if user_input:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Extract trip details
    starting_location, destination, days, preferences = extract_trip_details(user_input)
    budget, accessibility, accommodation, travel_dates, dietary_preference = extract_additional_details(user_input)
    
    if destination and days and preferences:
        itinerary = generate_itinerary(starting_location, destination, days, preferences, budget, accessibility, accommodation, travel_dates, dietary_preference)
    else:
        itinerary = "Could you provide more details? (e.g., 'Trip from Tokyo to Bali for 3 days, loves anime and food. Budget: luxury, Accessibility: wheelchair, Accommodation: mid-range, Travel Dates: 05/07/2025 to 08/07/2025, Diet: halal')"
    
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
