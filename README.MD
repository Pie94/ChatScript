# CommandAnalysis
## Python script to analyse how many times a set of command is executed into a Twitch chat
## By PieTheLemon

Every Twitch channel has a personal chat accessible through the IRC (Internet-Relay Chat) protocol.
This Python script exploits this connection to log the chat of a selected channel until it's closed.
At that point, it will analyze the chat log to see how many times a command, picked from a list of
command specified in a particular file, is executed in that Twitch chat. These counters are then
saved in a .csv files, with the counters sorted by decreasing values.

When opened, the program ask the user OAth key if not present. This key is an alphanumeric identificator
for the user to access the chat, representing their actual identity. When inserted, the code is saved
in an encripted file so that there's no need to ask for it again. 

The first part of the script connect to the desired Twitch chat and start logging it. The selected channel (and
other settings) can be inserted in the settings file. The log is managed by the *logging* module.

When the script is closed, it begin by loading the .csv file to get the actual value of the counters, i.e. the script is
able to store the counters and keep counting in different streams. Then the script analyses the saved log and check for
every message if the first word of a message is one of the commands written in the _command list_ file. For every command
encountered, the relative counter is incremented. When the script has parsed the whole chat log, it sorts the counters
ordered by decreasing values and export it to the .csv file, updating the values inside it.

The list of commands that need to be checked can be updated by adding and removing commands before/after the script has been executed;
adding a new command creates a new counter, naturally set to 0; deleting a command also deletes its counter, also removing it
from the .csv file the next time the user run the script.

## File structure
- CommandAnalysis.py:
- Settings.json
- CommandList.txt
- KeyAuth.

## Resources
- Twitch chat text stream: https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
- Twitch reference guide: https://dev.twitch.tv/docs/irc