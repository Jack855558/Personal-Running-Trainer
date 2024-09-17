import requests
import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize GPT-2 model and tokenizer
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

def fetch_strava_data(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://www.strava.com/api/v3/athlete/activities', headers=headers)
    data = response.json()
    return data

def preprocess_strava_data(data):
    df = pd.DataFrame(data)
    # Example calculations; adjust based on actual data fields
    weekly_mileage = df['distance'].sum() / 1000  # Convert meters to kilometers
    average_pace = df['moving_time'].mean() / df['distance'].mean()  # Example pace calculation
    recent_5k_time = "16:30"  # Placeholder; extract this from data
    return {
        'weekly_mileage': weekly_mileage,
        'average_pace': average_pace,
        'recent_5k_time': recent_5k_time
    }

def format_query(data):
    return (
        f"User data: Weekly mileage: {data['weekly_mileage']} km, "
        f"Average pace: {data['average_pace']} min/km, "
        f"Recent 5k time: {data['recent_5k_time']}. "
        "What adjustments should be made to improve the 5k time?"
    )

def generate_advice(query):
    inputs = tokenizer.encode(query, return_tensors='pt')
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    advice = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return advice
