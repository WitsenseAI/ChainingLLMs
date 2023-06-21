from moviepy.editor import ImageSequenceClip

# list of image file names to use in the video
image_files = ["imgs/test.jpg"]

# duration of the video clip in seconds
duration = 1

# create the video clip from the images and set its duration
clip = ImageSequenceClip(image_files, fps=1/duration)

# write the video clip to a file
clip.write_videofile("video.mp4", fps=24)
