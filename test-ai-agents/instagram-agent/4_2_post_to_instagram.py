"""
Posts an image to Instagram using the Meta Graph API.
The process involves three steps: creating a media container with the image URL,
polling until the container is ready, and finally publishing it to the feed.
Requires a public image URL (from Cloudinary) as Instagram does not accept direct file uploads.
"""

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
IG_USER_ID = os.getenv("INSTAGRAM_USER_ID")

def create_media_container(image_url: str, caption: str) -> str:
    url = f"https://graph.instagram.com/v25.0/{IG_USER_ID}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN,
    }
    response = requests.post(url, data=payload)
    data = response.json()

    if "id" in data:
        container_id = data["id"]
        print(f"Container created: {container_id}")
        return container_id
    else:
        print(f"Failed to create container: {data}")
        return None

def poll_container_status(container_id: str, max_attempts: int = 10) -> bool:
    url = f"https://graph.instagram.com/v25.0/{container_id}"
    params = {
        "fields": "status_code",
        "access_token": ACCESS_TOKEN,
    }

    for attempt in range(max_attempts):
        response = requests.get(url, params=params)
        status = response.json().get("status_code")
        print(f"Attempt {attempt + 1}: status = {status}")

        if status == "FINISHED":
            return True
        elif status == "ERROR":
            print("Container processing failed")
            return False

        time.sleep(5)  # wait 5 seconds between polls

    print("Timed out waiting for container")
    return False

def publish_container(container_id: str) -> bool:
    url = f"https://graph.instagram.com/v25.0/{IG_USER_ID}/media_publish"
    payload = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN,
    }
    response = requests.post(url, data=payload)
    data = response.json()

    if "id" in data:
        print(f"Posted successfully! Post ID: {data['id']}")
        return True
    else:
        print(f"Failed to publish: {data}")
        return False

def post_to_instagram(image_url: str, caption: str) -> bool:
    print("Step 1: Creating media container...")
    container_id = create_media_container(image_url, caption)
    if not container_id:
        return False

    print("Step 2: Waiting for container to be ready...")
    ready = poll_container_status(container_id)
    if not ready:
        return False

    print("Step 3: Publishing...")
    return publish_container(container_id)

# test with your image URL from previous step
post_to_instagram(
    image_url="https://res.cloudinary.com/dhinpomc5/image/upload/v1774013023/instagram-agent/gdolkxepadgszdzohjhd.jpg",  # paste your image URL here
    caption=("Tech"),  # replace with your caption
)
