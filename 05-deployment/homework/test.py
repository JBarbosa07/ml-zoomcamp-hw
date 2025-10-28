import requests

url = 'https://predict-convert.fly.dev/predict'

client = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

response = requests.post(url, json=client).json()

print('Response:', response)

if response['converted']:
    print('Client is likely to convert.')
else:
    print('Client is not likely to convert.')