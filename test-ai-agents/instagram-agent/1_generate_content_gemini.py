import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    generation_config={"response_mime_type": "application/json"}
)

SYSTEM_PROMPT = """
You are a content assistant for an Instagram avatar — a young woman who posts about
gym, outfits (OOTD), parties, functions, and trending dances.

Given a topic, return a JSON object with exactly these fields:
{
  "image_prompt": "A highly detailed prompt for an AI image generator. Must include:
    - Subject: stylish young woman, sharp facial features, long dark hair,
      athletic build, photorealistic, Instagram aesthetic
    - Specific outfit: describe clothing item, color, style
    - Exact pose and expression
    - Setting/background: specific location details
    - Lighting: e.g. golden hour, ring light, neon, natural window light
    - Mood: e.g. confident, playful, candid
    - Camera style: e.g. shot on iPhone 15 Pro, bokeh background, close-up",
  "caption": "2-3 sentences, conversational and punchy, relevant emojis, ends with a question or CTA",
  "hashtags": ["exactly 20 hashtags", "mix of niche-specific and medium tags", "no generic tags", "no hash symbol"]
}

Return only valid JSON. No explanation, no markdown, no code blocks.
"""

def generate_content(topic):
    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nTopic: {topic}")
    return json.loads(response.text)

result = generate_content("On the way to Japan")
print(json.dumps(result, indent=2))