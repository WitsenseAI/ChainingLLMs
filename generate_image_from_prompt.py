import openai
from dotenv import load_dotenv
import os
import urllib
import requests

def initialization():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

def img_from_prompt(prompt, img_name="gen.jpg"):
    initialization()
    no_of_imgs = 1 #st.number_input("Enter the number of images")
    if prompt:
        response = openai.Image.create(
            prompt=prompt,
            n=no_of_imgs,
            size="512x512"
        )
        if "data" in response:
            for key, obj in enumerate(response["data"]):
                filename ='image__generated'+str(key)+".jpg"
                urllib.request.urlretrieve(obj['url'], filename)
            print('Images have been downloaded and saved locally')
        else:
            print("Failed to generate image")
        image_url = response["data"][0]["url"]
        # st.image(image_url)
        request = requests.get(image_url, stream=True)
        img_path = os.path.join(os.path.join(os.getcwd(), "output"), img_name)
        with open(img_path, "wb+") as file:
            for c in request:
                file.write(c)


def __main__():
    test_prompt = "A portrait of the person walking into the lab, Sigma 85 mm f/1.4"
    img_from_prompt(test_prompt, img_name="gen1.jpg") 
    test_prompt = "A portrait of the person greeted by a friendly robot, , Sigma 85 mm f/1.4"
    "#Cut to a shot of a person looking up at the sky in awe"
    img_from_prompt(test_prompt, img_name="gen2.jpg")

if __name__ == "__main__":  
    __main__()