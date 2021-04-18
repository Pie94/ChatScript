import os
import sys
import json # to read/write json files
import csv # to read/write csv files
from cryptography.fernet import Fernet # to encrypt/decrypt the OAuth token
import socket # to open a connection with the IRC Twitch server
import logging # for logging the Chat strings
import re # for strings manipulation

""" Variable Definition """
settings_file = 'settings.json'
OAuth_file = 'KeyAuth'
settings = dict()
command_file = ''
commands_list = []
counter_sfx = dict()
data_file = ''
password = ''
OAuth = ''

""" Load settings file if it exists, otherwise use default settings and create a settings file """
settings_file = os.path.join(os.path.dirname(__file__), settings_file)
if os.path.isfile(settings_file):
        """ read settings """
        with open(settings_file, "r") as read_file:
            settings = json.load(read_file)      
else: # set default settings if no custom settings file is found
    settings = {
        'server': 'irc.chat.twitch.tv',
        'port': 6667,
        'nickname': 'PieTheLemon',
        'token': '',
        'channel': '#PieTheLemon'
    }
    with open(settings_file, "w") as write_file:
        json.dump(settings, write_file, sort_keys=True, indent=4)

""" Look for the KeyAuth file or ask for a new one """
if os.path.isfile(OAuth_file):
    f = Fernet(password)
    with open(OAuth_file, "rb") as read_file:
        OAuth = f.decrypt(read_file.write(OAuth_crypt))
    pass
    # Prompt for password
else:
    # Prompt for password
    # Prompt for OAuth Token
    f = Fernet(password)
    OAuth_crypt = f.encrypt(OAuth)
    with open(OAuth_file, "wb") as write_file:
        write_file.write(OAuth_crypt)
    pass

sock = socket.socket()
# Test connection
# try :
#     sock.connect((settings['server'], settings['port']))
# except 

sock.send(f"PASS {settings['token']}\n".encode('utf-8'))
sock.send(f"NICK {settings['nickname']}\n".encode('utf-8'))
sock.send(f"JOIN {settings['channel']}\n".encode('utf-8'))

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    handlers=[logging.FileHandler('ChatLog.txt', encoding='utf-8')])

try:
    while True:
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
    
        elif len(resp) > 0:
            logging.info(resp)
except KeyboardInterrupt:
    pass

""" Load Commands list.
    The command list must be a dictionary containing at least a 
    'Command' Key where the command name is defined. Streamlabs Chatbot allows to export
    groups of commands information into a file with extension .abcomg which is formatted
    in JSON """
command_file = os.path.join(os.path.dirname(__file__), 'CommandList')
if command_file and os.path.isfile(command_file):
    pass
    # ADD FILE READ
    
""" Load data file """
data_file = os.path.join(os.path.dirname(__file__), 'data_counter.csv')
""" Check if the data_file exists and if the Reset mode is set """
if data_file and os.path.isfile(data_file) and not settings['Reset']:
        """ read data """
        with open(data_file, "rb") as read_file:
            reader = csv.reader(read_file)
            next(reader, None)  # skip the header
            for row in reader:
                counter_sfx[row[0]] = int(row[1])
        
        # Check if a command has been deleted from the commands list
        # If a command from the database is not in the command list anymore,
        # it's value is cancelled
        for key in counter_sfx.keys():
            if key not in commands_list:
                counter_sfx.pop(key)
        
        # Check if there's a new command from the commands list which
        # in case is initialized
        for command in commands_list:
            if command not in counter_sfx:
                counter_sfx[command] = 0

else:   # initialize data for every command defined in the settings.json file
    for command in commands_list:
        counter_sfx[command] = 0
    """ If Reset is True, it sets is to False so that the next time the
        Script starts, it won't reset again """
    if settings['Reset']:
        """ Remove the Reset status """
        settings['Reset'] = False
        with open(settings_file, "w") as write_file:
            json.dump(settings, write_file, sort_keys=True, indent=4)

# if command_received in commands_list:
#             """ Increases the command counter related to the command executed """
#             counter_sfx[command_received] += 1

#   Sorting the counters
#   Extracting the keys and counters from the dictionary counter_sfx
keys = counter_sfx.keys()
counters = list(counter_sfx.values())
#   To sort the keys dictionary as the values, they are put in a tuple
#   (counters, keys) through the zip function. Then, we use the
#   sorted method to sort this list of tuples through the counters values.
#   Finally, we extract only the second element in the tuple, which is keys,
#   through the _, x command (_ is a placeholder that represent the first
#   element in the tuple, which is counters, that is ignored when sorting
#   the keys values)
keys = [x for _, x in sorted(zip(counters, keys), reverse=True)]
#   Sorting the counters value

#   Writing the sorted counters in the .csv file
with open(data_file, "wb") as write_file:
    writer = csv.writer(write_file)
    writer.writerow(["Command", "Counter"])
    for key in keys:
        writer.writerow([key, counter_sfx[key]])