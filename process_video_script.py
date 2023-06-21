"""
This script extracts scene prompts from video_script generated by llm.
Scene prompt are useful to generate the static images that can be generated by da
"""
import re
def find_title(filepath):
    with open(filepath, "r") as f:
        for line in f:
            line = line.replace("\n", "")
            line = re.sub(r"\"", "", line)
            return line
    return "No Title" 
def find_voiceover_lines(filepath):
    voiceover_lines = []
    with open(filepath, "r") as f:
        for line in f:
            voiceover_line = ""
            match1 = re.search(r"Voiceover(.*)", line)
            match2 = re.search(r"Narrator(.*)", line)
            if match1:
                line = f.__next__()
                voiceover_line = match1.group(1).strip()
            if match2:
                voiceover_line = match2.group(1).strip()
            if match1 or match2:
                voiceover_line = re.sub(r"[^a-zA-Z0-9]+", ' ', voiceover_line)
                voiceover_lines.append(voiceover_line)
            

    return voiceover_lines


def find_prompts(filepath):
    prompts = []
    with open(filepath, "r") as file:
        for line in file:
            #line = "Cut to a shot of stan looking up at the sky in awe"
            match1 = re.search(r"Cut to a shot of (.*)", line) or re.search(r"A shot of (.*)", line)
            match2 = re.search(r"Fade in to a (.*)", line)
            match3 = re.search(r"a shot of(.*)", line)
            match4 = re.search(r"The person is shown (.*)", line)
            if match1:
                extracted_text = match1.group(1)
                extracted_text = re.sub(r"[:,\[\]]", "", extracted_text)
                prompts.append(extracted_text+ ", Sigma 85 mm f/1.4")
            elif match2:
                extracted_text = match2.group(1)
                extracted_text = re.sub(r"[:,\[\]]", "", extracted_text)
                prompts.append(extracted_text+ ", Sigma 85 mm f/1.4")
            elif match3:
                extracted_text = match3.group(1)
                print("@@@@@@@@@", extracted_text)
                prompts.append(extracted_text+ ", Sigma 85 mm f/1.4")
            elif match4:
                extracted_text = match4.group(1)
                prompts.append("The person is shown" + extracted_text + ", Sigma 85 mm f/1.4")

    return prompts

