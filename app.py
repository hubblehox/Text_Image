import streamlit as st
import datetime
import openai
from base64 import b64decode
from openai.error import InvalidRequestError

def generate_image(prompt, num_image=1, size='512x512', output_format='url'):
    """
    params:
        prompt (str):
        num_image (int):
        size (str):
        output_format (str):
    """
    try:
        images = []
        response = openai.Image.create(
            prompt=prompt,
            n=num_image,
            size=size,
            response_format=output_format
        )
        if output_format == 'url':
            for image in response['data']:
                images.append(image.url)
        elif output_format == 'b64_json':
            for image in response['data']:
                images.append(image.b64_json)
        return {'created': datetime.datetime.fromtimestamp(response['created']), 'images': images}
    except InvalidRequestError as e:
        print(e)


# User input
prompt = st.text_input('Enter your prompt:')
num_image = st.number_input('Number of images:', min_value=1, max_value=5, value=1)
size = st.selectbox('Select size:', ('1024x1024', '512x512', '256x256'))
output_format = st.selectbox('Select output format:', ('url', 'b64_json'))

# Button to generate images
if st.button('Generate Images'):
    response = generate_image(prompt, num_image, size, output_format)
    if output_format == 'url':
        images = response['images']
        for image in images:
            st.image(image)  # Display the image in Streamlit
    elif output_format == 'b64_json':
        prefix = 'demo'
        for indx, image in enumerate(response['images']):
            file_path = f'{prefix}_{indx}.jpg'
            with open(file_path, 'wb') as f:
                f.write(b64decode(image))
            st.image(file_path)  # Display the image in Streamlit
