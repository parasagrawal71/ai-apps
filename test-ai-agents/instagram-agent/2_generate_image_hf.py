from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN"),
)

def generate_image(image_prompt: str, output_path: str = "output.png"):
    print("Generating image...")

    image = client.text_to_image(
        prompt=image_prompt,
        model="stabilityai/stable-diffusion-xl-base-1.0",
    )

    image.save(output_path)
    print(f"Saved to {output_path}")
    return output_path

generate_image(
    "A stylish young woman at an international airport, wearing an oversized "
    "beige trench coat over a cream knit sweater, paired with baggy cargo denim jeans and "
    "chunky white sneakers. Sitting in a first-class airplane window seat, glancing "
    "playfully at the camera with a warm smile, holding a matcha latte. Soft warm natural "
    "morning light, photorealistic, Instagram aesthetic, cinematic depth, shot on iPhone 15 Pro."
)