import tkinter as tk
from tkinter.ttk import *
import os
import pygame
from win32api import GetSystemMetrics
from moviepy.editor import *
from mutagen.mp3 import MP3
from PIL import ImageTk, Image
from random import *
from pytube import YouTube, Playlist
from time import *
import subprocess

# Add MP3 Downloader

# Fix time updating wrong incorrectly after paused.

# Fix shuffle from playing the same song twice in a row

# Add capability to add songs from other folders

# Add capability to move time scale to go to certain parts of a song


class MusicPlayer:

    def __init__(self, master, width, height, pauseImg, playImg, fastForwardImg, rewindImg, shuffleImg, backgroundImg):

        self.shuffled = False
        self.paused = False
        self.currentSong = -1

        # retrieves the path to each song in the MusicMasterFolder and stores them in a dictionary.
        #---------------------------------------------------------------------------------------------------------------
        self.musicD = {}
        directory = r"C:\MusicMasterFolder"
        num = 0
        for filename in os.listdir(directory):
            self.musicD[num] = (os.path.join(directory, filename))
            num += 1
        self.numSongs = len(self.musicD)
        #---------------------------------------------------------------------------------------------------------------

        # Adjusts the size of the listbox depending on the screens resolution
        #------------------------
        h = 30
        if width == 1920:
            h = 50
        #------------------------

        # Main Frame (contains song listbox)
        self.master = master
        self.title = tk.Label(self.master, text="Music Player", font="helvetica 25 bold", background="thistle3")
        self.frame = tk.Frame(self.master, background="thistle4")
        self.songListBox = tk.Listbox(self.frame, height=h, width=150, bd=5, background="thistle1")
        self.songListBox.grid(padx=10, pady=10, row=0, columnspan=3)

        # Inserts all of the songs into the main listbox
        #------------------------------------------
        for i in self.musicD:
            temp = self.musicD[i]
            temp = temp.split("\\")
            temp = temp[2]
            temp = temp[:-4]
            self.songListBox.insert("end", temp)
        #-------------------------------------------

        self.frame.grid(row=1, column=0)

        # stores the currents songs length
        self.songLength = 0


        # Button Frame
        #---------------------------------------------------------------------------------------------------------------
        self.buttonFrame = tk.Frame(self.master, background="thistle3")

        self.currentSongText = tk.Label(self.buttonFrame, font="helvetica 10", background="thistle3")
        self.currentSongText.grid(row=0, column=0)

        self.songDisplay = tk.Scale(self.buttonFrame, from_=0, to_=self.songLength, orient="horizontal", length=500, highlightbackground="thistle4", highlightthickness=3)
        self.songDisplay.grid(row = 1, column=0, padx=5, pady=(0, 20))

        self.rewindButton = tk.Button(self.buttonFrame, image=rewindImg, font="helvetica 10", command=self.play, background="white")
        self.rewindButton.grid(row=1, column=1, padx=5, pady=(0, 20))

        self.playButton = tk.Button(self.buttonFrame, image=playImg, font="helvetica 10", command=self.play, background="white")
        self.playButton.grid(row=1, column=2, padx=5, pady=(0, 20))

        self.fastForwardButton = tk.Button(self.buttonFrame, image=fastForwardImg, font="helvetica 10", command=self.skip, background="white")
        self.fastForwardButton.grid(row=1, column=3, padx=5, pady=(0, 20))

        self.pauseButton = tk.Button(self.buttonFrame, image=pauseImg, font="helvetica 10", command=self.pause, background="white")
        self.pauseButton.grid(row=1, column=4, padx=5, pady=(0, 20))

        self.shuffleButton = tk.Button(self.buttonFrame, image=shuffleImg, font="helvetica 10", command=self.shuffle, background="white")
        self.shuffleButton.grid(row=1, column=5, padx=5, pady=(0, 20))

        self.volumeText = tk.Label(self.buttonFrame, text="volume", font="helvetica 10", background="thistle3")
        self.volumeText.grid(row=0, column=6)

        self.volumeScale = tk.Scale(self.buttonFrame, from_=0, to_=100, orient="horizontal", highlightbackground="thistle4", highlightthickness=3, command=self.updateVolume)
        self.volumeScale.grid(row=1, column=6, padx=10, pady=(0, 20))

        self.songDownloaderButton = tk.Button(self.buttonFrame, text="Song Downloader", font="helvetica 10", command=self.new_window, background="white")
        self.songDownloaderButton.grid(row=1, column=7, padx=5, pady=(0, 20))

        self.buttonFrame.grid(row=2, column=0, pady=10)
        #---------------------------------------------------------------------------------------------------------------


        # Defaults the songs volume to zero
        pygame.mixer.music.set_volume(0)


    # called by the play button
    #-------------------------------------------------------------------------------------------------------------------
    def play(self):
        # gets the corresponding number to the selected song within the listbox
        selection1 = self.songListBox.curselection()
        selection = -1
        if selection1 != ():
            selection = selection1[0]

        if self.paused and self.currentSong == selection:
            pygame.mixer.music.unpause()
            self.pauseButton.config(background="white")
            self.updateTime()
        else:
            if selection1 != ():
                self.currentSong = selection
                song = MP3(r"" + self.musicD[selection])
                length = round(song.info.length)
                self.songLength = length
                self.songDisplay.config(from_=0, to_=self.songLength)
                pygame.mixer.music.load(r"" + self.musicD[selection])
                pygame.mixer.music.play()
                songTitle = self.songListBox.get(selection)
                self.currentSongText.config(text=songTitle)

                self.updateTime()
    #-------------------------------------------------------------------------------------------------------------------


    # called when the volume scale is adjusted
    #-------------------------------------------------------------------------------------------------------------------
    def updateVolume(self, volume):
        pygame.mixer.music.set_volume(int(volume) / 100)
    #-------------------------------------------------------------------------------------------------------------------


    # called by the skip button
    #-------------------------------------------------------------------------------------------------------------------
    def skip(self):
        if self.currentSong != -1:
            if not self.shuffled:
                self.songListBox.selection_clear(0, "end")
                self.songListBox.select_set(self.currentSong + 1)
                self.songListBox.activate(self.currentSong + 1)
                self.play()
            else:
                self.songListBox.select_clear(0, "end")
                num = randint(0, self.numSongs)
                self.songListBox.select_set(num)
                self.songListBox.activate(num)
                self.play()
    #-------------------------------------------------------------------------------------------------------------------


    #  called by the rewind button
    #-------------------------------------------------------------------------------------------------------------------
    def restart(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.rewind()
    #-------------------------------------------------------------------------------------------------------------------


    def shuffle(self):
        if not self.shuffled:
            self.shuffled = True
            self.shuffleButton.config(background="red")
        else:
            self.shuffled = False
            self.shuffleButton.config(background="white")


    # called by the pause button
    #-------------------------------------------------------------------------------------------------------------------
    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
            self.pauseButton.config(background="red")
    #-------------------------------------------------------------------------------------------------------------------


    # calls itself every second when a song is playing
    #-------------------------------------------------------------------------------------------------------------------
    def updateTime(self):
        if pygame.mixer.music.get_busy():
            pos = (round(pygame.mixer.music.get_pos() / 1000))
            self.songDisplay.set(pos)
            self.master.after(1000, self.updateTime)
            if pos == self.songLength:
                self.songListBox.selection_clear(0, "end")
                self.songListBox.select_set(self.currentSong + 1)
                self.songListBox.activate(self.currentSong + 1)
                self.play()
    #-------------------------------------------------------------------------------------------------------------------


    # Song Downloader Page
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = SongDownloaderPage(self.newWindow)


# Song Downloader
class SongDownloaderPage:
    def __init__(self, master):


        # Song Downloader Main Frame
        #---------------------------------------------------------------------------------------------------------------
        self.master = master
        self.frame = tk.Frame(self.master, width=700, height=500, background="thistle3")

        self.text1 = tk.Label(self.frame, text="This downloader works by taking songs/videos from YouTube via their URL and converting them to MP3 files.", background="thistle3", font="helvetica 9 bold")
        self.text1.grid(pady=(20, 0), padx=20)
        self.text2 = tk.Label(self.frame, text="The MP3 files are installed on your computer in a folder name MusicMasterFolder.", background="thistle3", font="helvetica 9 bold")
        self.text2.grid(pady=(5, 0))
        self.text3 = tk.Label(self.frame, text="The first time this program is ran the folder will automatically be created at path C:\MusicMasterFolder.", background="thistle3", font="helvetica 9 bold")
        self.text3.grid(pady=(5, 0))
        self.text4 = tk.Label(self.frame, text="This downloader can be used to install entire playlist or just individual songs.", background="thistle3", font="helvetica 9 bold")
        self.text4.grid(pady=(5, 0))



        self.playlistFrame = tk.Frame(self.frame,  background="thistle2", relief="raised", bd=10)

        self.text4 = tk.Label(self.playlistFrame, text="ENTER PLAYLIST URL", background="thistle2", font="helvetica 10 bold")
        self.text4.grid(pady=(8, 2))
        self.playlistUrlEntry = tk.Entry(self.playlistFrame, width=80)
        self.playlistUrlEntry.grid(pady=(0, 0), padx=10)
        self.playlistButton = tk.Button(self.playlistFrame, text="Download Playlist", font="helvetica 10", command=self.downloadPlaylist)
        self.playlistButton.grid(pady=(10, 10))

        self.playlistFrame.grid(pady=(30, 10))



        self.songFrame = tk.Frame(self.frame, background="thistle2", relief="raised", bd=10)

        self.text5 = tk.Label(self.songFrame, text="ENTER SONG URL", background="thistle2", font="helvetica 10 bold")
        self.text5.grid(pady=(8, 2))
        self.songUrlEntry = tk.Entry(self.songFrame, width=80)
        self.songUrlEntry.grid(pady=(0, 0), padx=10)
        self.songButton = tk.Button(self.songFrame, text="Download Song", font="helvetica 10", command=self.downloadSong)
        self.songButton.grid(pady=(10, 10))

        self.songFrame.grid(pady=(20, 20))


        self.progressBar = Progressbar(self.frame, orient="horizontal", length=200, mode="determinate")
        self.progressBar.grid(pady=(0, 30))




        self.frame.grid()

    #-------------------------------------------------------------------------------------------------------------------

    def downloadPlaylist(self):
        if len(self.playlistUrlEntry.get()) != 0:
            destination = r"C:\MusicTest"
            playlist = Playlist(self.playlistUrlEntry.get())
            numOfSongs = len(playlist)
            num = 100 / numOfSongs
            temp = 0



            for url in playlist:




                yt = YouTube(url)

                #stream = video.streams.get_lowest_resolution()
                #stream.download(output_path=out_dir, skip_existing=True)
                #mp4_path = out_dir + '/' + stream.default_filename

                video = yt.streams.get_lowest_resolution()
                out_file = video.download(output_path=destination)


                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)

                sleep(1)
                temp += num
                self.progressBar["value"] = temp
                self.master.update_idletasks()


    def downloadSong(self):
        if len(self.songUrlEntry.get()) != 0:

            self.progressBar["value"] = 20
            self.master.update_idletasks()

            destination = r"C:\MusicMasterFolder"
            yt = YouTube(self.songUrlEntry.get())
            video = yt.streams.filter(only_audio=True).first()

            self.progressBar["value"] = 40
            self.master.update_idletasks()

            out_file = video.download(output_path=destination)

            self.progressBar["value"] = 60
            self.master.update_idletasks()

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'

            self.progressBar["value"] = 80
            self.master.update_idletasks()

            os.rename(out_file, new_file)

            self.songButton.config(state="normal")

            self.progressBar["value"] = 100
            self.master.update_idletasks()








#-----------------------------------------------------------------------------------------------------------------------
def main():
    pygame.mixer.init()
    pygame.init()
    root = tk.Tk()

    root.state("zoomed")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # gets the resolution of the users monitor
    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    # opens all the icon images
    i1 = Image.open("icons8-pause-30.png")
    pauseImg = ImageTk.PhotoImage(i1)
    i2 = Image.open("icons8-fast-forward-30.png")
    fastForwardImg = ImageTk.PhotoImage(i2)
    i3 = Image.open("icons8-rewind-30.png")
    rewindImg = ImageTk.PhotoImage(i3)
    i4 = Image.open("icons8-play-30.png")
    playImg = ImageTk.PhotoImage(i4)
    i5 = Image.open("icons8-shuffle-32.png")
    shuffleImg = ImageTk.PhotoImage(i5)
    i6 = Image.open("background1.png")
    backgroundImg = ImageTk.PhotoImage(i6)

    # sets the size of the window to match the users resolution
    root.geometry(f"{screenWidth}x{screenHeight}")

    # sets the background of the root window
    root.config(background="thistle3")


    app = MusicPlayer(root, screenWidth, screenHeight, pauseImg, playImg, fastForwardImg, rewindImg, shuffleImg, backgroundImg)

    # refreshes the window
    root.mainloop()
#-----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    main()
