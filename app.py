from flask import Flask, render_template, request
import openai
##from openai import OpenAI
##client = OpenAI() 
import os
from dotenv import load_dotenv
##import base64

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        ##image_result = request.form["image_prompt"]
        try:
            response = openai.responses.create(
                model="gpt-4.1",  
                input=[{"role": "developer", "content": "Interpret dreams using Carl Jung’s analytical psychology, treating them as symbolic messages from the unconscious that draw on archetypes and the collective unconscious, and relating them to personal growth through individuation while speaking in a reflective, non-absolute tone.."}, 
                          {"role": "user", "content": prompt}],
                          temperature=1.7,
                          max_output_tokens=100
            )
            result = response.output_text

            ##img = client.images.generate(
            ##model="gpt-image-1",
            ##input=image_result,
            ##tools=[{"type": "image_generation"}],
            ##size="1024x1024"
            ##)

##image_bytes = base64.b64decode(img.data[0].b64_json)
##with open("output.png", "wb") as f:
    ##f.write(image_bytes)




if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing










