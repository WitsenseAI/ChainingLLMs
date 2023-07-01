"""
This script takes a topic of video from user,   and generates a video.
"""
import os
from generate_image_from_prompt import img_from_prompt
from process_video_script import find_title, find_voiceover_lines, find_prompts
from gtts import gTTS
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from moviepy.editor import *
from langchain.utilities import WikipediaAPIWrapper
import cv2
import streamlit as st
import json
from structured_video_script import structured_video_script
def initializeAPI():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")


def create_script(topic="Hello World", video_script_file="data/sample_video_script.txt", use_wikipedia=False):
    # prompt template declaration
    title_template = PromptTemplate(
        input_variables=["topic"],
        template="Write a title for the video on {topic}"
    )
    template_str = "Write a scene-by-scene video script for a video that has a title {title}"
    if use_wikipedia == True:
        template_str.append("using wikipedia pages {wikipedia_research}")
    script_template = PromptTemplate(
        # script to be generated from title 'and' wikipedia research
        input_variables=["title"],
        template = template_str)
        # template="Write a scene-by-scene video script using title {title}and referring wikipedia research {wikipedia_research}"

    structured_script_template_txt = """\
    For scene-by-scene video script: {script}, extract the following information for each scene as json:

    scene: for each scene, extract what the scene is about. For example, extract the scene description from scene transitions, and remove the additional details such as narrators, dialogues.
    scene_transition:  Extract  how the current scene is to be shown. For example, extract sentences such as  'cut to the scene...'  'The camera pans out ', 'fade in .. ', 'fade out...', etc.   
    voiceover: Extract voiceover, dialogs that narrator or any character is saying. If the sentence is said by a character such as Goldie:, then keep the name of character, but for narrator, remove it.

    Format the output JSON so that it has following keys:
    scene: [] 
    scene_transition: []
    voiceover: []

    """
    structured_script_template = ChatPromptTemplate.from_template(structured_script_template_txt)

    # memory setting to store the conversation
    title_memory = ConversationBufferMemory(
        input_key="topic", memory_key="chat_history")
    script_memory = ConversationBufferMemory(
        input_key="title", memory_key="chat_history")

    # LLM call
    llm = OpenAI(temperature=0.2, max_tokens=1000)
    chatGPTLLM = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2,)

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
    structured_script_chain = LLMChain(
        llm=llm,
        prompt=structured_script_template, #script_template,
        output_key="structured_script",
        verbose=True
    )

    generated_title = title_chain.run(topic)
    print("title", generated_title)
    if use_wikipedia:
        wiki = WikipediaAPIWrapper()
        wiki_research = wiki.run(topic)
        script_template.input_variables = ["title","wikipedia_research"]
        generated_script = script_chain.run(    
        title=generated_title, wikipedia_research=wiki_research)
    else:
        generated_script = script_chain.run(
        title=generated_title)
    
    structured_script = structured_script_chain.run(
        script=generated_script)
    structured_script = structured_script.replace("\n", "")
    # Remove newlines
    print("RAW structured script", structured_script)
    structured_script = structured_script.replace("Example Output:", "", 1)
    structured_script = structured_script.replace("Example JSON Output:", "", 1)
    print("RAW structured script", structured_script)
    with open(video_script_file , "w") as file:
        file.write(structured_script)
    base_name, _ = os.path.splitext(video_script_file)
    video_json_file = base_name + ".json"
    sscript_dict = json.loads(structured_script)
    video_script = {
        "title": generated_title,
        "scene": sscript_dict.get("scene"), # f"sscript_dict.get(\"scene\")",
        "scene_transition": sscript_dict.get("scene_transition"),
        "voiceover": sscript_dict.get("voiceover"),
    }
    with open(video_json_file, "w") as file:
        json.dump(video_script,file)


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




def script_to_clips(voiceover_lines,topic):
    script = ""
    clip_no= 0
    img_clips = []
    title_page = os.path.join("data","titlepg.jpg")
    image_list = ["output/"+f for f in os.listdir("output") if f.endswith(".jpg")]
    clip_no = 0
    clips = []
    audio_clips = []
    for aSentence in voiceover_lines:
        script =  aSentence  # .... are for pauses
        language = "en-gb"
        myobj = gTTS(text=script, lang=language, slow=False)
        audio_clip_path = "voiceover_clip" + str(clip_no) + ".mp3"
        myobj.save(audio_clip_path)
        try:
            print(audio_clip_path)
            audio_clip = AudioFileClip(str(audio_clip_path))
            if clip_no == 0:
                titleclip_duration =  3
                image_count = round(titleclip_duration * 24.0)  
                titleclip = ImageSequenceClip([title_page] * image_count, fps=24.0)
                titleclip = titleclip.set_duration(titleclip_duration) 
                image_count = round((audio_clip.duration -3)* 24.0)  
                # textclip = TextClip(script, fontsize=24, color="white", font="Arial", stroke_width=1, stroke_color="black", align="center", size=(512,512))
                # textclip = textclip.set_duration(textclip_duration)
                # clips.append(textclip)
                clip = ImageSequenceClip([image_list[clip_no]] * image_count , fps=24.0 )
                clip.set_duration(audio_clip.duration - titleclip_duration)
                clip0 =  concatenate_videoclips(clips=[titleclip, clip])
                clip0 = clip0.set_audio(audio_clip)
                clip0.set_duration(audio_clip.duration)
                clips.append(clip0)
                print("aud-video duration", audio_clip.duration, clip0.duration, clip.duration)    
            else:     
                clip = ImageSequenceClip([image_list[clip_no]] * image_count , fps=24.0)
                clip.set_duration(audio_clip.duration)
                clips.append(clip)
            # clip.duration = audio_clip.duration
                print("aud-video duration", audio_clip.duration, clip.duration)    
            clip_no = clip_no + 1
            audio_clips.append(audio_clip)
        except Exception as exception:
            print("failed to import audio clip!\n" + exception)
    print(len(clips), len(audio_clips))
    video = concatenate_videoclips(clips)
    # Set audio for the video
    audio = concatenate_audioclips(audio_clips)
    video = video.set_audio(audio)
    video_duration = audio.duration
    video.set_duration(video_duration)
    # Write the video clip to a file
    video.fps = 24.0
    output_file_path = os.path.join("output",f"{topic}.mp4")
    video.write_videofile(output_file_path)
    return output_file_path


    
def generate_images(prompts):
    no_of_imgs = 1  # st.number_input("Enter the number of images per prompt")
    for prompt in prompts:
        img_name = "image__generated"+str(no_of_imgs)+".jpg"
        no_of_imgs += 1
        img_from_prompt(prompt, img_name)

st.title("Video Script Generator")

form = st.form(key='my_form')
# text_input = form.text_input(label='Enter the prompt text')
text_input = "auroras"#"Story of Goldilocks and 3 bears"
submit_button = form.form_submit_button(label='Submit')
if submit_button:
    topic = text_input
    script_file_path = f"data/{topic}.txt"
    initializeAPI()
    #create_script(topic, script_file_path)
    base_name, _ = os.path.splitext(script_file_path)
    script_file_path_json = base_name + ".json"
    print(script_file_path_json)
    svs = structured_video_script(script_file_path_json, generation_style=None)
    title, prompts, voiceover_lines = svs.get_title(), svs.get_scene(), svs.get_voiceover()
    prompts.insert(0, title)
    voiceover_lines.insert(0, f"WitsenseAI presents a short video on {title}. This video is generated with the help of Open A.I. models - ChatGPT and DALL E 2")
    #generate_images(prompts=prompts)
    video_path = script_to_clips(voiceover_lines, topic)
    st.video(video_path, format="video/mp4", start_time=0)
    st.session_state["disabled"] = True

