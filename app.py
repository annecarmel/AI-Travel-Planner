import openai
import streamlit as st
import re
import requests

def extract_trip_duration(user_input):
    match = re.search(r'(\d+)\s*day', user_input, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 3  # Default to 3 days if not specified

def fetch_real_time_data(destination):
    search_url = f"https://api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US/anywhere/{destination}/anytime"  # Replace with real API key
    headers = {"apikey": "YOUR_SKYSCANNER_API_KEY"}
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_weather(destination):
    weather_url = f"https://api.weatherapi.com/v1/current.json?key=YOUR_WEATHER_API_KEY&q={destination}"
    response = requests.get(weather_url)
    if response.status_code == 200:
        return response.json().get('current', {}).get('condition', {}).get('text', "Weather data unavailable")
    return "Weather data unavailable"

def fetch_local_events(destination):
    events_url = f"https://www.eventbriteapi.com/v3/events/search/?location.address={destination}"  # Replace with real API key
    headers = {"Authorization": "Bearer YOUR_EVENTBRITE_API_KEY"}
    response = requests.get(events_url, headers=headers)
    if response.status_code == 200:
        events = response.json().get("events", [])
        return [event["name"]["text"] for event in events[:5]] if events else "No upcoming events."
    return "No local events found"

def get_travel_recommendations(user_input):
    trip_duration = extract_trip_duration(user_input)
    destination_match = re.search(r'to\s+([A-Za-z\s]+)', user_input, re.IGNORECASE)
    destination = destination_match.group(1).strip() if destination_match else "Unknown"
    
    real_time_data = fetch_real_time_data(destination)
    weather = fetch_weather(destination)
    local_events = fetch_local_events(destination)
    
    prompt = f"""
    You are an AI travel planner. Your task is to create a well-structured travel itinerary based on user preferences.
    
    Ask for missing details if needed, and provide a response in this format:
    
    **Destination:** {destination}
    **Travel Dates:** [User's travel dates]
    **Budget:** [User's budget]
    **Interests:** [Adventure, Beaches, Food, etc.]
    **Accommodation Preferences:** [Budget, Mid-range, Luxury]
    **Transport Mode:** [Flight, Train, Road Trip]
    **Special Requests:** [Vegetarian, Pet-friendly, etc.]
    
    Then, generate a **detailed {trip_duration}-day itinerary** with recommended places, activities, and food spots.
    
    Also, include the latest available travel options:
    
    **Flights & Hotels:** {real_time_data if real_time_data else "Could not fetch real-time data."}
    **Weather:** {weather}
    **Local Events:** {', '.join(local_events) if isinstance(local_events, list) else local_events}
    
    User Input: {user_input}
    AI Response:
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a structured AI travel planner."},
                  {"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

st.title("🌍 AI Travel Planner")
user_query = st.text_input("Tell me about your trip!")
if st.button("Plan My Trip!"):
    if user_query:
        response = get_travel_recommendations(user_query)
        st.markdown(response)
