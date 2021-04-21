# CommandAnalysis
Python script to analyse how many times a set of commands is executed into a Twitch chat.

## Introduction
Every Twitch channel has a personal chat accessible through the IRC (Internet-Relay Chat) protocol. This Python script exploits this connection to log the chat of a selected channel until it's closed. At that point, it will analyze the chat log to see how many times a command, picked from a list of command specified in a particular file, is executed in that Twitch chat. These counters are then saved in a .csv files, with the counters sorted by decreasing values.

When opened, the program ask the user OAth key if not present. This key is an alphanumeric identificator for the user to access the chat, representing their actual identity. When inserted, the code is saved in an encrypted file so that there's no need to ask for it again. The encryption is done through a passwordgiven by the user. This password is not saved locally, so the user needs to insert it every time they use thescript. The OAuth key can be reinserted if the KeyAuth file is removed manually (done when the script is not running). Here the script also asks if the user want to reset the Chat log (which can also be deleted manually by the user before running the script).

The first part of the script connect to the desired Twitch chat and start logging it. The selected channel (and other settings) can be inserted in the settings file. The log is managed by the **logging** module. Every once in a while, the script answer to a PING-PONG kind of check done by the Twitch IRC server to see if the script is still connected. The connection is wrapped in a SSL socket to ensure some form of encryption (since the OAuth key is sent to the server).

The logging fase can be interrupted by pressing CTRL + C (aka KeyboardInterrupt). Then the script loads the Commands list and the .csv file (if available) to get the actual value of the counters, i.e. the script is able to store the counters and keep counting in different streams. After that, the script analyse the saved log and check if every message's first word is one of the commands written in the Command list file. For every command encounter, the relative counter is incremented. When the script has parsed the whole chat log, it sorts the counters ordered by decreasing values and export it to the .csv file, updating the values inside it.

The list of commands that needs to be checked can be updated by adding and removing commands when the script is not running. Adding a new command creates a new counter, naturally set to 0, while deleting a command also deletes its counter, also removing it from the .csv file the next time the user run the script.

## Requirements
List of packages required (not available by default in Anaconda and probably on Python vanilla):
- pycryptodome (see https://pypi.org/project/pycryptodome/ for Anaconda)

This script has been tested on Python 3.8.8 installed through the Anaconda platform. It won't work properly on Python 2.7 or prior versions because of problems with the writing and reading functions in the csv module (the files should be read and written in binary format in that case).

## File structure
- CommandAnalysis.py: Script for the chat analysis
- encryption.py: encryption functions, used to encrypt the OAuth token before saving it to a file.
- Settings.json: Database with all the settings needed for the script. It's formatted to be human-readable since any change to the settings need to be done manually by the user in this file.
- CommandList.txt: List of commands. It must contain a list of keywords space-separated.
- KeyAuth: File containing the enctripted OAuth key that identifies the user accessing to the Chat.
- ChatLog.txt: where the chat is logged
## Settings file
The settings file is a json database, formatted to be easily readable, containing the main settings of the script:
- server: URL adress of the IRC chat; should be left as _'irc.chat.twitch.tv'_.
- port: Port adress of the IRC service. It should be 6697 for the SSL encrypted connection.
- nickname: the user's nickname, related to the OAuth key. It must be lowercase!
- channel: channel name you want to connect to. It should be formatted as _#channelname_ (e.g., #piethelemon).
- reset: if set to **true**, the script reset all the counter in the CommandCounter.csv file, then it set itself to false, so that the script won't reset itself the next time it will be executed; if set to **false**, the script will read all the counters saved in CommandCounter.csv if is available and use those values.
## CommandList file
The CommandList file contains a list of commands separated by whitespaces. The commands will be considered as not case-sensitive, so that _prova1_ and _Prova1_ will be counted in the same way.

E.g. of the file content:  
prova1 prova2  
prova3 prova4 prova5 prova6

Here both the space an return character count as whitespace.
## Resources
- Twitch OAuth generator: https://twitchapps.com/tmi/
- Twitch chat text stream: https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
- Twitch reference guide: https://dev.twitch.tv/docs/irc
- Encryption functions with a password: https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python
- RegExpr: https://docs.python.org/3/library/re.html#match-objects
- SSL wrapper for Python: https://docs.python.org/3/library/ssl.html
- logging module for Python: https://docs.python.org/3/library/logging.html
- csv file manipulation for Python: https://docs.python.org/3/library/csv.html
- json file manipulation for Python: https://docs.python.org/3/library/json.html
