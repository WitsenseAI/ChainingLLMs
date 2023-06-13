import os
from dotenv import load_dotenv

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

load_dotenv()
# os.getenv("OPENAI_API_KEY"))
api_key = os.getenv("OPENAI_API_KEY")

st.title("Youtube Video Script Generator")
prompt = st.text_input("Enter the prompt")

# prompt template declaration
title_template = PromptTemplate(
    input_variables=["topic"],
    template="Write a title for the video on {topic}"
)

script_template = PromptTemplate(
    input_variables=["title"],
    template="Write a video script for a video that has a title  {title}"
)


# LLM call
llm = OpenAI(temperature=0.2)

title_chain = LLMChain(
    llm=llm,
    prompt=title_template,
    output_key="title",
    verbose=True
)

script_chain = LLMChain(
    llm=llm,
    prompt=script_template,
    output_key="script",
    verbose=True
)

sequential_chain = SequentialChain(
    chains=[title_chain, script_chain],
    input_variables=["topic"],
    output_variables=["title", "script"],
    verbose=True
)
if prompt:
    # response = llm(prompt)
    # response = title_chain.run(topic=prompt)
    response = sequential_chain({"topic": prompt})
    st.write("Generated script:", response['title'], response['script'])
