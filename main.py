"""
This script takes a topic of video from user,   and generates a video.
"""
import os
from generate_image_from_prompt import img_from_prompt
from process_video_script import find_title, find_voiceover_lines, find_prompts
from gtts import gTTS
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from moviepy.editor import *
from langchain.utilities import WikipediaAPIWrapper
import cv2

def initializeAPI():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")


def create_script(topic="Hello World", video_script_file="data/sample_video_script.txt"):
    # prompt template declaration
    title_template = PromptTemplate(
        input_variables=["topic"],
        template="Write a title for the video on {topic}"
    )
    script_template = PromptTemplate(
        # script to be generated from title 'and' wikipedia research
        input_variables=["title"], #, 'wikipedia_research'],
        template="Write a video script for explanatory video that has a title {title}, describing each scene with details such as what is being shown, how it relates to the title {title}."
        #and by referring wikipedia for research {wikipedia_research}"
    )

    # memory setting to store the conversation
    title_memory = ConversationBufferMemory(
        input_key="topic", memory_key="chat_history")
    script_memory = ConversationBufferMemory(
        input_key="title", memory_key="chat_history")

    # LLM call
    llm = OpenAI(temperature=0.2, max_tokens=3300)
    chatGPTLLM = ChatOpenAI(model_name="gpt-3.5-turbo")

    # define chains
    title_chain = LLMChain(
        llm=chatGPTLLM,
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
    generated_title = title_chain.run(topic)
    print("title", generated_title)
    wiki = WikipediaAPIWrapper()
    wiki_research = wiki.run(topic)
    generated_script = script_chain.run(
        title=generated_title) #, wikipedia_research=wiki_research)
    with open(video_script_file, "w") as file:
        file.write(generated_title)
        file.write(generated_script)


def get_script(video_script_file="data/sample_video_script.txt"):
    script = ""
    with open(video_script_file, "r") as file:
        for line in file:
            script += line
    return script


def script_to_voice(voiceover_lines):
    script = ""
    for aSentence in voiceover_lines:
        script = script + aSentence + " \n"
    print("##script", script)
    language = "en-gb"
    myobj = gTTS(text=script, lang=language, slow=False)
    myobj.save("mytext2speech.mp3")

def encodeImage(data):
    #resize inserted image
    data= cv2.resize(data, (512,512))
    # run a color convert:
    data= cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    return bytes(data) #encode np array to Bytes string




def script_to_audio_clips(voiceover_lines):
    script = ""
    clip_no= 0
    img_clips = []
    image_list = ["output/"+f for f in os.listdir("output") if f.endswith(".jpg")]
    clip_no = 0
    clips = []
    audio_clips = []
    for aSentence in voiceover_lines:
        script =  aSentence + " ...." # .... are for pauses
        language = "en-gb"
        myobj = gTTS(text=script, lang=language, slow=False)
        audio_clip_path = "voiceover_clip" + str(clip_no) + ".mp3"
        myobj.save(audio_clip_path)
        try:
            audio_clip = AudioFileClip(str(audio_clip_path))
            print(audio_clip.duration)        
            clip = ImageSequenceClip([image_list[clip_no]], fps=1/audio_clip.duration)
            clip_no = clip_no + 1
            clips.append(clip)
            audio_clips.append(audio_clip)
        # if i < num_images - 1:
        #     pause_clip = AudioClip(duration=pause_duration)
        #     clips.append(pause_clip)
        except Exception as exception:
            print("failed to import audio clip!\n" + exception)
    video = concatenate_videoclips(clips)
    # Set audio for the video
    audio = concatenate_audioclips(audio_clips)
    video = video.set_audio(audio)
    video_duration = audio.duration
    video = video.set_duration(video_duration)
    # Write the video clip to a file
    video.write_videofile("output/video.mp4")


    
def generate_images(prompts):
    no_of_imgs = 1  # st.number_input("Enter the number of images")
    for prompt in prompts:
        img_name = "image__generated"+str(no_of_imgs)+".jpg"
        no_of_imgs += 1
        img_from_prompt(prompt, img_name)


def main():
    topic = "Artemis"
    script_file_path = "data/artemis.txt"
    initializeAPI()
    # #create_script(topic, script_file_path)
    title= find_title(script_file_path)
    # print("Title: ",title)
    # prompts = find_prompts(script_file_path)
    # prompts.insert(0,"Generate a photorealistic image for " + title + " Sigma 26 mm f/1.4") 

    # print("~~~~~~~~~~~~",prompts)
    # generate_images(prompts=prompts)
    voiceover_lines = find_voiceover_lines(script_file_path)
    voiceover_lines.insert(0, title)
    # print(len(voiceover_lines),len(prompts))
    print("Voiceover lines:~~~~~~~~~",voiceover_lines)
    #script_to_voice(voiceover_lines)
    script_to_audio_clips(voiceover_lines)


if __name__ == "__main__":
    main()
