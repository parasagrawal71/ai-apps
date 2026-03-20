import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv
import base64
import io

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_image_as_part(image_path: str) -> dict:
    with open(image_path, "rb") as f:
        image_data = f.read()
    ext = image_path.split(".")[-1].lower()
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    return {
        "inline_data": {
            "mime_type": mime,
            "data": base64.b64encode(image_data).decode("utf-8")
        }
    }

def generate_image(image_prompt: str, reference_paths: list, output_path: str = "output.png"):
    model = genai.GenerativeModel("gemini-3.1-flash-image-preview")

    # build content: reference images first, then the prompt
    content = []
    for path in reference_paths:
        content.append(load_image_as_part(path))

    content.append({
        "text": (
            f"Using the person in the reference image(s) above as the character, "
            f"generate a new Instagram-style photo with this scene:\n\n{image_prompt}\n\n"
            f"Keep the same face, skin tone, and general appearance. "
            f"Only the outfit, pose, and background should change."
        )
    })

    response = model.generate_content(content)

    # extract image from response
    for part in response.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            image_data = base64.b64decode(part.inline_data.data)
            image = Image.open(io.BytesIO(image_data))
            image.save(output_path)
            print(f"Image saved to {output_path}")
            return output_path

    print("No image in response. Response text:", response.text)
    return None

generate_image(
    image_prompt=(
        "A stylish young woman at an international airport, wearing an oversized "
        "beige trench coat over a cream knit sweater, paired with baggy cargo denim jeans and "
        "chunky white sneakers. Sitting in a first-class airplane window seat, glancing "
        "playfully at the camera with a warm smile, holding a matcha latte. Soft warm natural "
        "morning light, photorealistic, Instagram aesthetic, cinematic depth."
    ),
    reference_paths=[
        "references/gemini_front.png",   # your main avatar photo
        "references/front_2.png",
        "references/full_body.png",
        "references/left_side.png",
        "references/right_side.png",
        "references/using_phone.png",
    ],
    output_path="output/output.png"
)