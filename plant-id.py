#!/usr/bin/env python3
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from wand.image import Image as WandImage
import os

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)

def disable_identify_plant():
    st.session_state["identify_plant"] = False

def enable_identify_plant():
    st.session_state["identify_plant"] = True

#st.title("Identify a Plant")
st.set_page_config(page_title="Identify a Plant", page_icon=":camera:", layout="centered")
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

    with WandImage( blob=st.session_state["uploaded_file"].getvalue()) as wand_image:
        
        preview_width = 300

        img_buffer = numpy.asarray(bytearray(wand_image.make_blob(format='png')), dtype='uint8')
        bytesio = io.BytesIO(img_buffer)
        image = PILImage.open(bytesio)
        st.image(image, caption="Uploaded Image", width=preview_width)