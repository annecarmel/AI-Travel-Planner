import os
import openai

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OpenAI API key is missing.")
    exit(1)

openai.api_key = api_key

# Example API call (Modify as needed)
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

print(response["choices"][0]["message"]["content"])
