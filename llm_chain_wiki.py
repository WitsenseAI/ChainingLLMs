import os
from dotenv import load_dotenv

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

from langchain.utilities import WikipediaAPIWrapper

load_dotenv()
# os.getenv("OPENAI_API_KEY"))
api_key = os.getenv("OPENAI_API_KEY")

st.title("Video Script Generator")
prompt = st.text_input("Enter the prompt")

# prompt template declaration
title_template = PromptTemplate(
    input_variables=["topic"],
    template="Write a title for the video on {topic}"
)

script_template = PromptTemplate(
    input_variables=["title", 'wikipedia_research'], #script to be generated from title 'and' wikipedia research   
    template="Write a video script for a video that has a title {title} using wikipedia pages {wikipedia_research}"
)

# memory setting to store the conversation
title_memory = ConversationBufferMemory(input_key="topic", memory_key="chat_history")
script_memory = ConversationBufferMemory(input_key="title", memory_key="chat_history")

# LLM call
llm = OpenAI(temperature=0.2)

title_chain = LLMChain(
    llm=llm,
    prompt=title_template,
    output_key="title",
    memory=title_memory,
    verbose=True
)

script_chain = LLMChain(
    llm=llm,
    prompt=script_template,
    output_key="script",
    memory=script_memory,
    verbose=True
)

# sequential_chain = SequentialChain(
#     chains=[title_chain, script_chain],
#     input_variables=["topic"],
#     output_variables=["title", "script"],
#     verbose=True
# )

"""
With two separate chains defined, we can use wiki wrapper to join
"""
wiki = WikipediaAPIWrapper()

if prompt:
    generated_title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    generated_script = script_chain.run(title=generated_title, wikipedia_research=wiki_research)    
    st.write("Title:", generated_title)
    st.write("Script:", generated_script)
    # with st.expander("Title History"):
    #     st.info(title_memory.buffer)
    # with st.expander("Script History"):
    #     st.info(script_memory.buffer)
    # with st.expander("Wiki Research History"):
    #     st.info(wiki_research)
