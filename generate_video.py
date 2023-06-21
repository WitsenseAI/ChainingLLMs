from moviepy.editor import *

# Load audio file
audio = AudioFileClip("output/mytext2speech.mp3")

# Load sequence of images
image_list = ["output/"+f for f in os.listdir("output") if f.endswith(".jpg")]

image_sequence = ImageSequenceClip(image_list, fps=24)

# Load sequence of images
# image_sequence = ImageSequenceClip(["path/to/image1.png", "path/to/image2.png", "path/to/image3.png"], fps=24)

# Set duration of each image and pause
image_duration = 2.0  # seconds
pause_duration = 1.0  # seconds

# Calculate the total duration of the video
num_images = len(image_list)
total_duration = num_images * (image_duration + pause_duration) - pause_duration

# Create a list of clips for each image and pause
clips = []
for i, image in enumerate(image_sequence):
    image_clip = image.set_duration(image_duration)
    clips.append(image_clip)
    if i < num_images - 1:
        pause_clip = AudioClip(duration=pause_duration)
        clips.append(pause_clip)

# Combine clips into a video
video = concatenate_videoclips(clips)

# Set audio for the video
video = video.set_audio(audio)

# Set duration of the video to match the duration of the audio
video_duration = audio.duration
video = video.set_duration(video_duration)

# Write the video clip to a file
video.write_videofile("output/video.mp4")


