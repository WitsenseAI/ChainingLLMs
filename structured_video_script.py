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
    def __init__(self, file_path):
        with open(file_path, "r") as file:
            self.data = json.load(file)

    def get_title(self):
        return self.data["title"]

    def get_scene(self):
        return self.data["scene"]

    def get_scene_transition(self):
        return self.data["scene_transition"]
    
    def get_voiceover(self):
        return self.data["voiceover"]
    