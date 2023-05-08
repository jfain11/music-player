from moviepy import editor
from pytube import YouTube, Playlist
import os


YOUTUBE_URL = 'https://www.youtube.com'

def download_mp3(video: YouTube) -> str:
    """
    Downloads the audio of a YouTube video in MP3 format.
    :param video: The video from which to download the audio
    :param config: The configuration settings for the download
    :return: The path of the newly created mp4 file
    """

    out_dir = r"C:\MusicTest"
    # returns the mp4 only containing audio
    stream = video.streams.get_lowest_resolution()
    stream.download(output_path=out_dir, skip_existing=True)
    mp4_path = out_dir + '/' + stream.default_filename
    return mp4_path

def convert_mp4_to_mp3(path: str, delete_after: bool = True) -> str:
    """
    Converts an mp4 file to an mp3 file
    :param path: The path of the mp4 file
    :param delete_after: If false, the mp4 file will not be deleted after conversion
    :return: The path of the newly created mp3 file
    """
    mp3_path = f'{path[:-3]}mp3'  # changes "mp4" to "mp3"
    mp4 = editor.VideoFileClip(path)
    mp3 = mp4.audio
    mp3.write_audiofile(mp3_path)

    mp3.close()
    mp4.close()

    os.remove(path)




playlist = Playlist("https://www.youtube.com/playlist?list=PL6W6WKRda0KbYFefDSE6AkHVe5XVIZOo3")
for video in playlist.videos:
    path = download_mp3(video)

    convert_mp4_to_mp3(path)
    print("ok")
print("done")

