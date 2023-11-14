import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from moviepy.editor import *
import re
import os

def convert_video_to_mp3():
    link = link_entry.get()

    # Check that the link is a valid YouTube link
    if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link):
        result_label.config(text="Error: Invalid YouTube link")
        return

    # Extract the video ID from the link
    video_id = None
    if "/watch?v=" in link:
        video_id = link.split("/watch?v=")[1][:11]
    elif "/v/" in link:
        video_id = link.split("/v/")[1][:11]
    elif "youtu.be/" in link:
        video_id = link.split("youtu.be/")[1][:11]

    if not video_id:
        result_label.config(text="Error: Unable to extract video ID from link")
        return

    try:
        yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream as a .mp4 file
        audio_file = audio_stream.download()

        # Use moviepy to convert the .mp4 file to a .mp3 file
        audio_clip = AudioFileClip(audio_file)
        audio_clip.write_audiofile(audio_file[:-4] + ".mp3")

        # Remove the original .mp4 file
        os.remove(audio_file)

        result_label.config(text="Conversion complete!")
    except Exception as e:
        result_label.config(text="Error: " + str(e))

# Create the main window
root = tk.Tk()
root.title("YouTube to MP3 Converter")
root.geometry("500x500")

# Create and place widgets
label = ttk.Label(root, text="Enter YouTube Link:",font=('seif',20))
label.pack(pady=10)

link_entry = ttk.Entry(root, width=50)
link_entry.pack()

convert_button = ttk.Button(root, text="Convert to MP3", command=convert_video_to_mp3)
convert_button.pack(pady=25)

result_label = ttk.Label(root, text="")
result_label.pack()

# Start the GUI main loop
root.mainloop()