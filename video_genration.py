import os
from dotenv import load_dotenv
import urllib3
import urllib.request
import requests

import cv2
import openai
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

from langchain.utilities import WikipediaAPIWrapper


def img_from_prompt(prompt, img_name="gen.jpg"):
    #prompt = st.text_input("Enter the image to be generated")
    print("generating image from prompt {}".format(prompt))
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
        st.image(image_url)
        request = requests.get(image_url, stream=True)
        with open(img_name, "wb+") as file:
            for c in request:
                file.write(c)
                
load_dotenv()
# os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Video  Generator")
prompt = st.text_input("Enter the topic")

# prompt template declaration
title_template = PromptTemplate(
    input_variables=["topic"],
    template="Write a title for the video on {topic}"
)

script_template = PromptTemplate(
    input_variables=["title", 'wikipedia_research'], #script to be generated from title 'and' wikipedia research   
    template="Write a video script for a video that has a title {title} and by referring wikipedia for research {wikipedia_research}"
)

dalle_template = PromptTemplate(
    input_variables=["script"], #script to be generated from title 'and' wikipedia research   
    template="Write a description of each scene for a video that has a script {script}"
)
# memory setting to store the conversation
title_memory = ConversationBufferMemory(input_key="topic", memory_key="chat_history")
script_memory = ConversationBufferMemory(input_key="title", memory_key="chat_history")
# dalle_memory = ConversationBufferMemory(input_key="script", memory_key="chat_history")

# LLM call
llm = OpenAI(temperature=0.2)

title_chain = LLMChain(
    llm=llm,
    prompt=title_template,
    output_key="title",
    memory=title_memory,
    verbose=True
)
if prompt:
    generated_title = title_chain.run(prompt)
    print("title",generated_title)
    #img_from_prompt(generated_title, img_name="title.jpg")

#if title_template:

script_chain = LLMChain(
    llm=llm,
    prompt=script_template,
    output_key="script",
    memory=script_memory,
    verbose=True
)

wiki = WikipediaAPIWrapper()

if prompt:
    wiki_research = wiki.run(prompt)
    generated_script = script_chain.run(title=generated_title, wikipedia_research=wiki_research)    
    print('script_template', generated_script)
    # number_of_lines = 0 
    # for line in generated_script:
    #     number_of_lines += 1
    #     img_name = "img{}.jpg".format(number_of_lines)
    #     print("{}: {}".format(number_of_lines, line.strip()))
    #     img_from_prompt(line.strip(), img_name=img_name)
       
dalle_chain =  LLMChain(
    llm=llm,
    prompt=dalle_template,
    output_key="dalle_gen_img",
    # memory=dalle_memory,
    verbose=True
)

if prompt:
    generated_prompt_for_dalle = dalle_chain.run(prompt)
    print('generated_prompt_for_dalle', generated_prompt_for_dalle)
    st.write("Script:", generated_script)
    st.write("prompt for dalle:", generated_prompt_for_dalle)