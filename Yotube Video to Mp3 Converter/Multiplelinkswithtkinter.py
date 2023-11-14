from pytube import YouTube
from moviepy.editor import *
import os
import re
import tkinter as tk
from tkinter import Entry, Button, Label, Text, END, Scrollbar, Y
from tkinter import filedialog

# Create a tkinter window
window = tk.Tk()
window.title("YouTube Audio Downloader")
window.geometry("500x500")

# Create a label and entry field for entering YouTube links
label = Label(window, text="Enter YouTube Links (one per line):")
label.pack()

entry = Text(window, width=50, height=10)
entry.pack()

# Create a function to download and convert audio when the button is clicked
def download_audio():
    links = entry.get("1.0", "end-1c").splitlines()
    
    for link in links:
        link = link.strip()

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
            mp3_file = audio_file[:-4] + ".mp3"
            audio_clip.write_audiofile(mp3_file)

            # Remove the original .mp4 file
            os.remove(audio_file)

            result_text.insert(tk.END, f"Conversion complete for {link}\n")

            # Add a link to open the file explorer for the converted audio
            result_text.tag_config("link", foreground="blue", underline=1)
            result_text.insert(tk.END, f"Click here to open '{mp3_file}' in File Explorer\n", "link")
            result_text.tag_bind("link", "<Button-1>", lambda event, file=mp3_file: open_in_explorer(file))
        except Exception as e:
            result_text.insert(tk.END, f"Error for {link}: {e}\n")

# Create a button to start the download and conversion process
download_button = Button(window, text="Download & Convert Audio", command=download_audio)
download_button.pack()

# Create a label to display results
result_label = Label(window, text="Results:")
result_label.pack()

# Create a text widget for displaying results with a scrollbar
result_text = Text(window, width=50, height=10)
result_text.pack()

scrollbar = Scrollbar(window, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Function to open the file explorer
def open_in_explorer(file_path):
    os.system(f"explorer /select, \"{file_path}\"")
    

# Start the tkinter main loop
window.mainloop()
