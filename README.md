## Goal- Demo LLM workflow with Langchain -

1. How  prompt templates can be used effectively to save users the hassle to write elaborate prompts.

2. How to do simple chaining operation with [LangChain](https://python.langchain.com/en/latest/index.html) where output from LLM can be used as input to query other service such as wikipedia

 
For demo, let us create a simple streamlit app where a user can enter the topic that interests them as a prompt. The app will use langchain and LLMs (depending on configuration) to generate title and script for the topic, and present to user. 

The prompt may look like -

```
Write me a youtube video title about ------------
```

LangChain prompt templates help to automate the prompt structuring behind the scene so that the user can simply enter only the topic in place of  -------------
This feature of LangChain is quite useful to improve prompting, as the user need not know how to efficiently structure the prompt.


## Installation of requisites (tested on Ubuntu 22.04LTS)

```
git clone https://github.com/suvarnak/ChainingLLms.git
conda create -n "llm_env" python=3.8
conda activate llm_env
pip install streamlit langchain openai==0.27.0 tiktoken wikipedia chroma python-dotenv
pip install opencv-python moviepy pysrt gTTS
sudo apt-get install espeak 
sudo apt install imagemagick -y
```
Create a `.env` file and paste your API key in it.


## To run the app 
The script `llm_chian.py` forms a simple sequential chain that generates a title for the topic entered by user, and from generated title and user-entered topic, generates the video script.

```
streamlit run llm_chain.py

```

The script `llm_chain_wiki.py` uses a wrapper for Wikipedia python library 

## To run the app
```
streamlit run llm_chain_wiki.py

```

The script `main.py` generates a video on any topic using llm (gpt-3.5-turbo), langchain,  Google text-to-speech, DallE2,  moviepy to create image-video with narration. You can choose if the video generation should refer to data source such as wikipedia for more informative video.

```
streamlit run main.py
```

## Demo output  for simple LLM + Wiki prompt chaining

![Simple Chaining with Langchain](imgs/langchain_demo.png)

## Demo output for single-click video generation where the user enters only the topic!
