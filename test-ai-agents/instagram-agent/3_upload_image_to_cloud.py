"""
Uploads a local image to Cloudinary and returns its public URL.
Cloudinary is used as image hosting because Instagram API requires
a public URL to fetch the image from, rather than a direct file upload.

Tried these too:
- IMGUR: Couldn't signup due to server load
- ImgBB: Generated public URL is too slow
"""

import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(image_path: str) -> str:
    result = cloudinary.uploader.upload(
        image_path,
        folder="instagram-agent",
        resource_type="image",
        format="jpg",          # force JPEG
        quality="auto:good",   # auto compress
        fetch_format="auto",
    )
    url = result["secure_url"]
    print(f"Uploaded: {url}")
    return url

upload_image("output.png") # Update file path
