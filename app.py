import openai
import streamlit as st

def get_travel_recommendations(user_input):
    prompt = f"""
    You are a travel AI assistant. The user wants to plan a trip. Gather details like:
    - Destination
    - Budget range
    - Travel dates
    - Interests (e.g., adventure, beaches, food, history, etc.)
    - Preferred transport (flight, train, road trip)
    - Accommodation preferences (budget, mid-range, luxury)
    - Special requests (vegetarian food, pet-friendly hotels, etc.)

    Based on this, generate a structured response to guide the user.
    
    User: {user_input}
    AI:"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful AI travel planner."},
                  {"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

st.title("🌍 AI Travel Planner")
user_query = st.text_input("Tell me about your trip!")
if st.button("Plan My Trip!"):
    if user_query:
        response = get_travel_recommendations(user_query)
        st.write(response)
