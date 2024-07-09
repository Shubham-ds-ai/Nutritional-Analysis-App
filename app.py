import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure API with the key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image_data):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt] + image_data)
    return response.text

def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        image_data = [{"mime_type": upload_file.type, "data": bytes_data}]
        return image_data
    else:
        raise FileNotFoundError("No file uploaded")
    
# Initialize Streamlit app
st.set_page_config(page_title="Meal Calorie Counter")
st.header("Meal Calorie Counter")
st.title('Nutritional Analysis App')

upload_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
image = None

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Check the total calories")

input_prompt = """
You are an expert in nutrition where you need to see the food items from the image
and calculate the total calories and provide the approximate Protein, Carbohydrate, Fats quantity in that meal
and also provide the details of every food items with calories intake in below tabular format:

1. Item 1 name- Approx. calories = , Approx. Protein Intake =  , Approx. Carbohydrate Intake = , Approx. Fat Intake = 
2. Item 2 name- Approx. calories = , Approx. Protein Intake =  , Approx. Carbohydrate Intake = , Approx. Fat Intake = 
----
----
"""

if submit and upload_file is not None:
    image_data = input_image_setup(upload_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("The Response is")
    st.write(response)
