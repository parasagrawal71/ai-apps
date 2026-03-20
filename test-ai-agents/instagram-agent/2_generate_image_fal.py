
import fal_client
import requests
import os, base64
from dotenv import load_dotenv

load_dotenv()
os.environ["FAL_KEY"] = os.getenv("FAL_API_KEY")

def image_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    ext = path.split(".")[-1]
    return f"data:image/{ext};base64,{data}"

def generate_image(image_prompt: str, output_path: str = "output.png"):
    # Use your best reference photo (add more paths to the list for better consistency)
    reference_images = [
        image_to_data_uri("references/gemini_front.png"),
        image_to_data_uri("references/full_body.png"),
        image_to_data_uri("references/left_side.png"),
        image_to_data_uri("references/right_side.png"),
    ]

    result = fal_client.submit(
        "fal-ai/ip-adapter-face-id",
        arguments={
            "prompt": image_prompt,
            "image_url": reference_images[0],   # primary reference
            "num_inference_steps": 40,
            "guidance_scale": 7.5,
            "face_id_weight": 0.8,               # how strongly to preserve face
            "num_images": 1,
        }
    ).get()

    image_url = result["images"][0]["url"]
    img_data = requests.get(image_url).content
    with open(output_path, "wb") as f:
        f.write(img_data)
    print(f"Saved to {output_path}")
    return output_path

generate_image(
    "A stylish woman at an international airport, wearing an oversized "
    "beige trench coat over a cream knit sweater, paired with baggy cargo denim jeans and "
    "chunky white sneakers. Sitting in a first-class airplane window seat, glancing "
    "playfully at the camera with a warm smile, holding a matcha latte. Soft warm natural "
    "morning light, photorealistic, Instagram aesthetic, cinematic depth, shot on iPhone 15 Pro."
)