from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import base64
from openai import OpenAI
from uuid import uuid4

load_dotenv()  # Load environment variables from .env

# Create static folder if missing (important on Render)
os.makedirs("static", exist_ok=True)

# Use ONE client style (recommended)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

DEV_PROMPT = (
    "Interpret dreams using Carl Jung’s analytical psychology, treating them as symbolic "
    "messages from the unconscious that draw on archetypes and the collective unconscious, "
    "and relating them to personal growth through individuation while speaking in a reflective, "
    "non-absolute tone."
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_path = None

    if request.method == "POST":
       
        try:
            prompt = request.form.get("prompt", "").strip()
            if not prompt:
                return render_template("index.html", result="Please enter a dream.", image_path=None)

          # ---- TEXT ----
            text_resp = client.responses.create(
                model="gpt-4.1",
                input=[
                    {"role": "developer", "content": DEV_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=1.5,
                max_output_tokens=150,
            )
            result = text_resp.output_text

            # ---- IMAGE ----
            img_resp = client.images.generate(
                model="gpt-image-1",
                prompt=f"Surreal symbolic dream imagery, cinematic lighting, mystical atmosphere, detailed illustration: {prompt}",
                size="1024x1024",
            )

            if not img_resp.data or not img_resp.data[0].b64_json:
                raise RuntimeError("Image API returned no base64 data.")

            image_bytes = base64.b64decode(img_resp.data[0].b64_json)
            image_path = f"output_{uuid4().hex}.png"
            with open(os.path.join("static", image_path), "wb") as f:
                f.write(image_bytes)

        except Exception as e:
            # This prints the REAL error into Render logs
            print("ERROR in POST:", repr(e))
            result = f"Error: {str(e)}"
            image_path = None

    return render_template("index.html", result=result, image_path=image_path)


if __name__ == "__main__":
    app.run(debug=True)
