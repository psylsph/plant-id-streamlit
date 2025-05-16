#!/usr/bin/env python3
from email import message
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from wand.image import Image as WandImage
from PIL import Image as PILImage
from json_repair import loads as repair_json_loads
import numpy
import base64
import io
import os

# Load environment variables from .env file
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def disable_identify_plant():
    st.session_state["identify_plant"] = False

def enable_identify_plant():
    st.session_state["identify_plant"] = True

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


st.set_page_config(page_title="Identify a Plant", page_icon=":camera:", layout="centered")
st.title("Identify a Plant")
st.html("""
    <style>
        .stMainBlockContainer {
            max-width:21rem;
        }
    </style>
    """
)

if "identify_plant" not in st.session_state:
    st.session_state["identify_plant"] = True

st.session_state["uploaded_file"] = st.file_uploader("**Select an image...**", type=["jpg", "jpeg", "png", "heic"], on_change=enable_identify_plant)

if st.session_state["uploaded_file"] is not None:

    with st.spinner("Identifying Plant...", show_time=True):

        with WandImage( blob=st.session_state["uploaded_file"].getvalue()) as wand_image:
            
            preview_width = 300

            img_buffer = numpy.asarray(bytearray(wand_image.make_blob(format='png')), dtype='uint8')
            bytesio = io.BytesIO(img_buffer)
            image = PILImage.open(bytesio)
            image.save("plant.jpg")
            st.image(image, caption="Uploaded Image", width=preview_width)

            message = """What plant in this image?
                        1. Be specific in the type
                        2. Give a score of certainty of out 100%
                        3. Give a detailed description
                        4. Provide care information and conditions the plant likes
                        Format your response as JSON with the following structure:
                        {{
                            "name": "plant name",
                            "certainty": "out of 100",
                            "description": "a description of the plant",
                            "care": "care and conditions information for the plant",
                        }}"

                    """

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": message},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encode_image("plant.jpg")}",
                                },
                            },
                        ],
                    }
                ],
                model="meta-llama/llama-4-scout-17b-16e-instruct",
            )

            json = repair_json_loads(chat_completion.choices[0].message.content)

            st.markdown("Name: " + json.get("name"))
            st.markdown("Certainty: " + json.get("certainty"))
            st.markdown("Description: " + json.get("description"))
            st.markdown("Care: " + json.get("care"))