import openai
import streamlit as st
import re
import requests
import time

def extract_trip_duration(user_input):
    match = re.search(r'(\d+)\s*day', user_input, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 3  # Default to 3 days if not specified

def fetch_real_time_data(destination):
    try:
        API_KEY = "YOUR_SKYSCANNER_API_KEY"
        if API_KEY == "YOUR_SKYSCANNER_API_KEY":
            return "API key missing. Please update your API key."
        search_url = f"https://api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US/anywhere/{destination}/anytime"
        headers = {"apikey": API_KEY}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching real-time travel data: {str(e)}"

def fetch_weather(destination):
    try:
        API_KEY = "YOUR_WEATHER_API_KEY"
        if API_KEY == "YOUR_WEATHER_API_KEY":
            return "API key missing. Please update your API key."
        weather_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={destination}"
        response = requests.get(weather_url)
        response.raise_for_status()
        return response.json().get('current', {}).get('condition', {}).get('text', "Weather data unavailable")
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"

def fetch_local_events(destination):
    try:
        API_KEY = "YOUR_EVENTBRITE_API_KEY"
        if API_KEY == "YOUR_EVENTBRITE_API_KEY":
            return "API key missing. Please update your API key."
        events_url = f"https://www.eventbriteapi.com/v3/events/search/?location.address={destination}"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(events_url, headers=headers)
        response.raise_for_status()
        events = response.json().get("events", [])
        return [event["name"]["text"] for event in events[:5]] if events else "No upcoming events."
    except requests.exceptions.RequestException as e:
        return f"Error fetching local events: {str(e)}"

def get_travel_recommendations(user_input):
    trip_duration = extract_trip_duration(user_input)
    destination_match = re.search(r'to\s+([A-Za-z\s]+)', user_input, re.IGNORECASE)
    destination = destination_match.group(1).strip() if destination_match else "Unknown"
    
    real_time_data = fetch_real_time_data(destination)
    time.sleep(1)  # To prevent rate limiting
    weather = fetch_weather(destination)
    time.sleep(1)
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
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a structured AI travel planner."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

st.title("🌍 AI Travel Planner")
user_query = st.text_input("Tell me about your trip!")
if st.button("Plan My Trip!"):
    if user_query:
        response = get_travel_recommendations(user_query)
        st.markdown(response)
