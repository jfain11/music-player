from pytube import YouTube
from pytube import Playlist
import os
import moviepy.editor as mp
import re

url = str(input("Enter Playlist URL"))
playlist = Playlist(url)

for url in playlist:
    print(url)
    YouTube(url).streams.filter(only_audio=True).first().download(r"C:\Users\jacob\Desktop\music temp")




