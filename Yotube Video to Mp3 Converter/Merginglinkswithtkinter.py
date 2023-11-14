from pytube import YouTube
from moviepy.editor import *
import os
import re
import tkinter as tk
from tkinter import Entry, Button, Text, Scrollbar

# Create a tkinter window
window = tk.Tk()
window.title("YouTube Audio Downloader")

# Create a label and entry field for entering YouTube links
label = tk.Label(window, text="Enter YouTube Links (one per line):")
label.pack()

entry = Text(window, height=10, width=50)
entry.pack()

# Create a function to download and convert audio when the button is clicked
def download_audio():
    links = entry.get("1.0", "end-1c").split('\n')
    audio_clips = []

    for link in links:
        # Check that the link is a valid YouTube link
        if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link):
            result_text.insert(tk.END, f"Error: Invalid YouTube link: {link}\n")
            continue

        # Extract the video ID from the link
        video_id = None
        if "/watch?v=" in link:
            video_id = link.split("/watch?v=")[1][:11]
        elif "/v/" in link:
            video_id = link.split("/v/")[1][:11]
        elif "youtu.be/" in link:
            video_id = link.split("youtu.be/")[1][:11]

        if not video_id:
            result_text.insert(tk.END, f"Error: Unable to extract video ID from link: {link}\n")
            continue

        # Create a YouTube object and extract the audio stream
        try:
            yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
            audio_stream = yt.streams.filter(only_audio=True).first()

            # Download the audio stream as a .mp4 file
            audio_file = audio_stream.download()

            # Use moviepy to convert the .mp4 file to a .mp3 file
            audio_clip = AudioFileClip(audio_file)
            audio_clips.append(audio_clip)  # Add the audio clip to the list

            # Remove the original .mp4 file
            os.remove(audio_file)

            result_text.insert(tk.END, f"Conversion complete for {link}\n")
        except Exception as e:
            result_text.insert(tk.END, f"Error for {link}: {e}\n")

    # Merge all audio clips into one
    merged_audio = concatenate_audioclips(audio_clips)
    merged_audio.write_audiofile("merged_audio.mp3")
    result_text.insert(tk.END, "Merging complete!\n")

# Create a button to start the download and conversion process
download_button = Button(window, text="Download & Convert Audio", command=download_audio)
download_button.pack()

# Create a text box to display results
result_text = Text(window, height=10, width=50)
result_text.pack()

# Create a scrollbar for the result text box
scrollbar = Scrollbar(result_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

# Start the tkinter main loop
window.mainloop()
