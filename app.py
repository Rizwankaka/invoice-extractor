from dotenv import load_dotenv
load_dotenv() # load all the environment variables from .env 

import streamlit as st 
import os # for picking up the environment variable 
from PIL import Image 
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load Gemini Flash 
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Initializing our streamlit app 
st.set_page_config(page_title='Multilanguage Invoice Extractor')

input_prompt = """
You are an expert in understanding invoices. We will upload an image as invoice 
and you will have to answer any questions based on the uploaded invoice image
"""

st.title('Multilanguage Invoice Extractor')

uploaded_file = st.file_uploader('Choose an image of the invoice...', type=['jpg', 'jpeg', 'png'])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

input = st.text_input('Ask a question about the invoice:', key='input')

submit = st.button('Analyze Invoice')

# If submit button is clicked
if submit:
    if uploaded_file is None:
        st.error("Please upload an image first.")
    elif not input:
        st.error("Please ask a question about the invoice.")
    else:
        with st.spinner("Analyzing the invoice..."):
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input)
            st.subheader("Analysis Result")
            st.write(response)