#!/usr/bin/env python
# SHOUT SHOUT SHOUT
# by andri
import sys
import re
from random import choice

# This script is executed every time a PRIVMSG happens
# Get PRIVMSG from arguments
msg = ' '.join(sys.argv[3:])
nick = sys.argv[1]

# Checks if input is greater than 5 characters and if input doesn't have lowercase letters
if len(msg) > 5 and msg == msg.upper(): #and msg == re.compile(s'\W{n,}'):
    # Open the shout database
    with open('data/shoutdb', 'r+') as f:
        shouts = f.read().split('\n')
        # Return a random shout from the database
        print choice(shouts)
        # If the shout is not a duplicate, add it to the database
        # Ignores the last cell because it's an empty string
        if msg not in shouts[:-1]:
            f.write(msg + '\n')
