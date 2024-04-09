import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
left_co, cent_co,last_co = st.columns(3)
with cent_co:
      st.image('mits-logo.png', caption='Madhav Institute of Technology and Sciences,Gwalior')
st.title('Image Caption Generator')
radio_input=st.radio(
    "Do you want to upload a image or capture a new one",
    [":rainbow[Upload]", "Capture:movie_camera:"],
    captions = ["Make Sure you have it in your machine", "Say Cheese"]
    )
if radio_input==':rainbow[Upload]':
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if radio_input=='Capture:movie_camera:':
    uploaded_file = st.camera_input("Take a picture")


API_KEY ="AIzaSyC4uKuTHWkFxFwpNkP6lmhsc1C7yQjreK8"
if uploaded_file is not None:
    if st.button('Upload'):
        if API_KEY.strip() == '':
            st.error('Enter a valid API key')
        else:
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            img = Image.open(file_path)
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-pro-vision')
                caption = model.generate_content(["Write a caption for the image in english",img])
                tags=model.generate_content(["Generate 5 hash tags for the image in a line in english",img])
                description=model.generate_content(["Describe the various details in the image",img])
                st.image(img, caption=f"Caption: {caption.text}")
                st.write(f"Tags: {tags.text}")
                st.write(f"Description:{description.text}")
            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    st.error("Invalid API Key. Please enter a valid API Key.")
                else:
                    st.error(f"Failed to configure API due to {error_msg}")
footer="""
  <style>
        a:link, a:visited {
            color: blue;
            text-decoration: dotted; /* Remove underline */
        }

        a:hover, a:active {
            color: skyblue;
        }
        .footer .p{
            font-size:10px;
        }

        /* Footer */
        .footer {
            position:fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height:10%;
            font-size:15px;
            color: white; 
            text-align: center;
            padding: 10px 0; 
        }
        .footer p{
            font-size:20px;
        }

        .footer a:hover {
            color: white;
        }
    </style>

    <div class="footer">
        <p><a href="https://www.linkedin.com/in/dhruv-charne-908848213/?originalSubdomain=in" target="_blank">Dhruv Charne</a></p>
    </div>
"""
st.markdown(footer,unsafe_allow_html=True)
