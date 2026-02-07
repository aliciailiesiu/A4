from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import base64
from openai import OpenAI

client = OpenAI()

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_path = None

    if request.method == "POST":
        prompt = request.form["prompt"]

        try:
            response = openai.responses.create(
                model="gpt-4.1",  
                input=[
                    {
                        "role": "developer",
                        "content": "Interpret dreams using Carl Jung’s analytical psychology, treating them as symbolic messages from the unconscious that draw on archetypes and the collective unconscious, and relating them to personal growth through individuation while speaking in a reflective, non-absolute tone."}, 
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.5,
                    max_output_tokens=150
            )

            result = response.output_text


            img = client.images.generate(
                model="gpt-image-1",
                prompt=f"Surreal symbolic dream imagery, cinematic lighting, mystical atmosphere, detailed illustration: {prompt}",
                n=1,
                size="auto"
            )

            image_bytes = base64.b64decode(img.data[0].b64_json)
            image_path = "static/output.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, image_path=image_path)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing