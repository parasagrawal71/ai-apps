import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
IG_USER_ID = os.getenv("INSTAGRAM_USER_ID")

def test_connection():
    url = f"https://graph.instagram.com/v25.0/{IG_USER_ID}"
    params = {
        "fields": "id,username,biography,followers_count",
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        print(f"Error: {data['error']['message']}")
    else:
        print("Connected successfully!")
        print(f"Username: {data.get('username')}")
        print(f"Followers: {data.get('followers_count')}")

test_connection()