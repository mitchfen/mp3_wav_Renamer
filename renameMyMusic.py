''' TODO 
-need to be able to detect redundant names to avoid overwrite
    easy way would be to check name you want to write it as against the files[] list
-add mechanism to detect if sox is installed on Manjaro
    os.system("pacman -Q sox")
    then read in the bash output
-Add functionality to move to sub directories within Music folder
-Add convenient way to count songs in directory and see progress working through them
'''
import re
import os
import sys
import subprocess
from pathlib import Path
from colorama import Fore, Style

'''
Not going to be as simple as I thought
The files[i] or "pathToSong" is the full path including the name and extension
need to trip off the original song name and append the new one, 
then check that resulting string against files[] AND because files[] is never updated, need to keep track of names in second list
and check this new name against that list as well

# here files[i] is passed as pathToSong 
def ensureNoOverwrite(files, pathToSong, newName):
    for i in range(len(files)):
        newPath = pathToSong + newName
'''

def renameSong(pathToSong, newName):            
    print(Fore.RED + "Renaming to " + newName)    # want to confirm rename in red
    print(Style.RESET_ALL)
    # mv bash command must recieve two arguments in quotes
    cmd = ("mv " + "\"" + pathToSong + "\"" + " " + "\"" + newName + "\"")
    os.system(cmd)

def getMusicDirectory():
    # Ask user where the music is stored
    print (Fore.GREEN + "\nHello, I will help you rename your music.")
    print ("Please enter the directory your music is in.")
    print ("Enter it like: /home/username/music\n")
    print(Style.RESET_ALL)
    print (Fore.BLUE + "Directory: ", end = "")   # want input on same line, different color
    print(Style.RESET_ALL, end = "")
    musicDir = input()
     #Ensure directory is valid and ends in a backslash
    if musicDir[len(musicDir)-1] != "/":
        musicDir += "/"
    assert os.path.exists(musicDir), "ERROR "+str(musicDir) + " is an invalid directory"
    return musicDir

def sanitizeSongName(nameToCheck):
    # ensure that name the user wants does not contain weird characters
    # only spaces and alphanumerics are allowed
    # multiple spaces are allowed but seriously.. don't do that
    keepGoing = True
    while(keepGoing):
        y = re.search("^[a-zA-Z0-9\s]+$", nameToCheck)
        if(y):
            keepGoing = False
        else:
            print("Error this is not a valid name")
            nameToCheck = input("Please try again: ")
    return nameToCheck

def playAndTakeInput(musicDir, files = []):
    for i in range(len(files)-1):
        # I want the sox output to be yellow so I can distinguish from my python
        print (Fore.YELLOW) 
        # need to wrap file names in quotes so bash can read them properly
        os.system("play " + "\"" + files[i] + "\"")
        print(Style.RESET_ALL)
        print("Name this file(x to delete, k to keep) do not include extension.")
        uncheckedName = input("Name: ")
        # pass the desired name to check it before continuing
        songName = sanitizeSongName(uncheckedName)

        if songName== "x":
                cmd = ("rm " + "\"" + files[i] + "\"")
                os.system(cmd)     
                print(Fore.RED + "Deleted.")
                print(Style.RESET_ALL)
        elif songName == "k":
                print(Fore.RED + "Keeping file as " + files[i])
                print(Style.RESET_ALL)
        else:

            if files[i][len(files[i])-1] == "3": # mp3 file
                songName = musicDir + songName + ".mp3"
                renameSong(files[i], songName)
            elif files[i][len(files[i])-1] == "v": # wav file
                songName = musicDir + songName + ".wav"
                renameSong(files[i], songName)
            else:
                print(Fore.RED + "Renaming to") 
            
def collectSongs(musicDir, files = []):
    # Walk the directory and build list of files
    for (path, dirnames, filenames) in os.walk(musicDir):
        files.extend(os.path.join(path, name) for name in sorted(filenames))
    return files

# Its not silly if it works
musicDir = getMusicDirectory()
files = []
files = collectSongs(musicDir, files)
playAndTakeInput(musicDir, files)