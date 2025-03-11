from pytube import YouTube
import tkinter as tk
from tkinter import filedialog

def download_vid(file_path, url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        highest_resolution = streams.get_highest_resolution()
    except Exception as e:
        print(e)

