import os
import sys
import json # to read/write json files
import csv # to read/write csv files
from getpass import getpass
import socket # to open a connection with the IRC Twitch server
import ssl # to create 
import logging # for logging the Chat strings
import re # for strings search
import encryption # contains the encryption functions

""" Variable Definition """

settings_file = 'settings.json'
OAuth_file = 'KeyAuth'
chat_log_file = 'ChatLog.txt'
settings = dict()
command_file = 'CommandList.txt'
commands_list = []
counter_sfx = dict()
data_file = 'CommandCounter.csv'
password = ''
OAuth = ''

""" Initialization Process """

channel = input("Enter the channel name you want to connect to: ").lower()
# Load settings file if it exists, otherwise use default settings,
# and create a settings file
settings_file = os.path.join(os.path.dirname(__file__), settings_file)
if os.path.isfile(settings_file):
        # read settings
        with open(settings_file, "r") as read_file:
            settings = json.load(read_file)
else: # set default settings if no custom settings file is found
    nickname = input("Enter your Twitch nickname: ").lower() # it must be lowercase!
    settings = {
        'server': 'irc.chat.twitch.tv',
        'port': 6697,
        'nickname': nickname,
        'reset': False
    }
    with open(settings_file, "w") as write_file:
        json.dump(settings, write_file, sort_keys=True, indent=4)

# Look for the KeyAuth file or ask for a new one
if os.path.isfile(OAuth_file):
    try:
        password = getpass("Insert the password: ")
        with open(OAuth_file, "r") as read_file:
            OAuth = encryption.decrypt(password.encode('utf-8'), read_file.read()).decode('utf-8')
    except ValueError:
        sys.exit('\nWrong password!')
else:
    OAuth = input("Enter the OAuth token: ")
    password = getpass(
        "Insert a password (used to access the OAuth token when stored):\n")
    OAuth_crypt = encryption.encrypt(password.encode('utf-8'), OAuth.encode('utf-8'))
    with open(OAuth_file, "w") as write_file:
        write_file.write(OAuth_crypt)

reset_chatlog = 'n'
if os.path.isfile(chat_log_file):
    reset_chatlog = input("Reset the Chat log? (y/n)\n").lower()
    counter = 0
    while reset_chatlog not in ['y', 'n']:
        counter += 1
        if counter == 3:
            sys.exit('Incorrect input at chat log reset')
        print('Incorrect input. Try again!')
        reset_chatlog = input("Reset the Chat log? (y/n)").lower()


# Load Commands list. The command list must be a series of commands
# separated by spaces (e.g., "prova1 prova2 prova3")
command_file = os.path.join(os.path.dirname(__file__), command_file)
if command_file and os.path.isfile(command_file):
    with open(command_file,'r') as read_file:
        commands_list = read_file.read().split()
else:
    sys.exit('\nCommandList file not found. Exiting!')

""" Connection to the IRC chat and Logging phase """

# Connection to the IRC chat
try:
    sock =  socket.socket(socket.AF_INET)
    context = ssl.create_default_context()
    conn = context.wrap_socket(sock, server_hostname=settings['server'])
    conn.connect((settings['server'],settings['port']))
    conn.sendall(f"PASS {OAuth}\n".encode('utf-8'))
    conn.sendall(f"NICK {settings['nickname']}\n".encode('utf-8'))
    conn.sendall(f"JOIN #{channel}\n".encode('utf-8'))
except Exception as e:
    print(f'\nConnection error:\n{e}')
    del password
    del OAuth
    sys.exit()

if reset_chatlog == 'y':
    logging.basicConfig(level=logging.DEBUG,
            format='%(message)s',
            handlers=[logging.FileHandler(chat_log_file, encoding='utf-8',
            mode='w')])
else:
    logging.basicConfig(level=logging.DEBUG,
            format='%(message)s',
            handlers=[logging.FileHandler(chat_log_file, encoding='utf-8')])


# Logging until the CTRL + C (KeyboardInterrupt) command is given
try:
    while True:
        msg = conn.recv(2048).decode('utf-8')
        print(msg)
        
        if msg.startswith('PING'):
            conn.sendall("PONG\n".encode('utf-8'))
        elif len(msg) > 0:
                logging.info(msg)
except KeyboardInterrupt:
    # Close the connection to the IRC channel
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

# Remove the password and OAuth variables for security reason, since they're
# not needed anymore
del password
del OAuth

""" Analysis of the ChatLog file """
    
# Load data file
data_file = os.path.join(os.path.dirname(__file__), data_file)
# Check if the data_file exists and if the Reset mode is set
if data_file and os.path.isfile(data_file) and not settings['reset']:
        # read data
        with open(data_file, "r") as read_file:
            reader = csv.reader(read_file)
            next(reader, None)  # skip the header
            for row in reader:
                counter_sfx[row[0]] = int(row[1])
        
        # Check if a command has been deleted from the commands list
        # If a command from the database is not in the command list anymore,
        # it's value is cancelled
        for key in list(counter_sfx.keys()):
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
    # If Reset is True, it sets is to False so that the next time the
    # Script starts, it won't reset again
    if settings['reset']:
        # Remove the Reset status
        settings['reset'] = False
        with open(settings_file, "w") as write_file:
            json.dump(settings, write_file, sort_keys=True, indent=4)

# ChatLog parsing and counter increment if a command has been inserted
# the opened file (log variable) is an iterable object, so I can
# iterate through all its lines
with open(chat_log_file,'r') as log:
    for line in log:
        message = re.search(
                ':.*\!.*@.*\.tmi\.twitch\.tv PRIVMSG #.* :(.*)', line)
        if message:
            command = message.group(1).split()[0].lower()
            if command in commands_list:
                counter_sfx[command] += 1

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
with open(data_file, "w") as write_file:
    writer = csv.writer(write_file)
    writer.writerow(["Command", "Counter"])
    for key in keys:
        writer.writerow([key, counter_sfx[key]])
