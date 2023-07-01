"""
This script extracts scene prompts from structured video script generated with LLM + Langchain prompt.

videoscript: 
{   
    "title": "",
    "scene": [],
    "scene_transition": [],
    "voiceover": []
}
"""

import json
import json

class structured_video_script:
    # generation_style = {"placement" = "after", "prompt_text" = "Sigma 85 mm f/1.4, "}
    style = {"place" : "before", "prompt_text" : "A water color painting  of"}
     
    def __init__(self, file_path, generation_style):
        if generation_style is not None:
            self.style = generation_style
        with open(file_path, "r") as file:
            self.data = json.load(file)

    def get_title(self):
        return self.data["title"]

    def get_scene(self):
        modified_prompts = []
        for prompt_txt in self.data["scene"]:
            if self.style["place"] == "before":
                prompt_txt =  self.style["prompt_text"] + prompt_txt 
            elif self.style["place"] == "after":
                prompt_txt = prompt_txt + self.style["prompt_text"]
            modified_prompts.append(prompt_txt)
        return modified_prompts
    def get_scene_transition(self):
        return self.data["scene_transition"]
    
    def get_voiceover(self):
        return self.data["voiceover"]
    