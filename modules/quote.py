#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Show a quote of someone that you've seen
# by andri
from sys import argv
from random import choice

# Directory where logs are
logdir = "logs/"
# Get channel and nick from raw irc data
data = argv[1]
if len(argv) == 3: # If no arguments are found, it gets the nick from the raw data
    nick = data[1:data.find('!')]
else: 
    nick = argv[3] # If an argument is found, it gets the nick from the first argument
channel = data.split(' ')[2].replace('/','-') # Gets the channel from the data and replaces slashes with dashes

# Assumes that the logs are in the log directory with the same name as the channel, but slashes are replaced with dashes
with open(logdir+channel) as f:
    # Turns the log into a list
    f = f.read().split('\n')
    # Filters the log, so that only the lines of the nick remain
    # This might need to be changed depending on the log layout
    # Lowering both, so the nicks aren't case sensitive
    f = filter(lambda x: '\t'+nick.lower()+'\t' in x.lower(), f)
    # If the log is empty, the nick hasn't been seen talking
    if len(f) > 0:
        msg = choice(f) # Gets a random line from the log
        date = msg.split(' ')[0] # Gets the date
        print date, '<'+msg[20:].replace('\t','> ') # Returns the date, skips the time and returns the rest of the line
    else:
        print "Sorry, I haven't seen %s say anything." %nick 
