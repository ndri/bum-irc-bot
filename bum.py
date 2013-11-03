#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bum-irc-bot v0.1
import socket
import sys
import os
from subprocess import Popen, PIPE
from glob import glob
from datetime import datetime

# CHANGE THESE
network = 'irc.rizon.net'
botnick = 'nick'
channels = ['#channel1', '#channel2']
password = 'password' # Leave blank if you don't want to identify
prefixes = ['.', ',', ':', ';', '!', '>', '~'] # Only 1-byte prefixes, sorry
filecommands = {
    'py': 'python',
    'rb': 'ruby',
    'lua': 'lua'
}

def parsedata(data):
    nick = data[1:data.find('!')]
    try: 
        signal = data.split()[1]
        channel = data.split()[2].replace('/','_').strip(':')
    except IndexError:
        signal = ''
        channel = ''
    message = ''
    if signal in signals:
        if signal == signals[0]:
            message = data[data.find(channel)+len(channel)+2:]
        elif signal in signals[1:2]:
            message = data[data.find(channel)+len(channel)+2:]
        elif signal == signals[3]:
            channel = channel[1:]
        elif signal in signals[4:5]:
            message = data[data.find(channel)+len(channel)+1:]
    return nick, signal, channel, message

def log(nick, signal, channel, message):
    out = ''
    time = str(datetime.now())[:19]
    with open('logs/%s' %channel, 'a') as f:
        if signal == signals[0]:
            out = '%s\t%s\t%s' %(time, nick, message)
        elif signal in signals[1:2]:
            out = '%s\t<<<\t%s (%s)' %(time, nick, message)
        elif signal == signals[3]:
            out = '%s\t>>>\t%s' %(time, nick)
        elif signal in signals[4:5]:
            out = '%s\t---\t%s %s %s' %(time, nick, signal, message)
        if out:
            f.write(out + '\n')
            print channel + '\t' + out

def privmsg(channel, message):
    messages = message.strip('\n').replace('[me]','\x01ACTION').split('\n')
    for msg in messages:
        irc.send('PRIVMSG %s :%s\n' %(channel, msg))
        log(botnick, 'PRIVMSG', channel, msg)

signals = ['PRIVMSG', 'PART', 'QUIT', 'JOIN', 'KICK', 'MODE']

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((network, 6667))

irc.send('NICK %s\n' %botnick)
irc.send('USER %s %s %s :%s\n' %(botnick, botnick, botnick, botnick))

for channel in channels:
    irc.send('JOIN %s\n' %channel)

data = irc.recv(256)[:-2]

if password:
    irc.send('PRIVMSG NickServ :IDENTIFY %s\n' %password)

while True:
    data = irc.recv(256)[:-2]
    if data[:4] == 'PING':
        irc.send('PONG' + data[4:])
    else:
        nick, signal, channel, message = parsedata(data)
        if signal in signals:
            log(nick, signal, channel, message)
        if signal == 'PRIVMSG' and message[0] in prefixes:
            command = glob('modules/' + message.split()[0][1:] + '.*')
            if command:
                command, extension = command[0][8:].split('.')
                args = message.split()[1:]
                popenargs = [filecommands[extension], 'modules/%s.%s' %(command,extension), data, nick] + args
                try:
                    moduleout = Popen(popenargs, stdout=PIPE).stdout.read()
                    privmsg(channel, moduleout)
                except: 
                    print 'error'

        if signal == 'PRIVMSG' and message != '' and nick != 'py-ctcp':
            for trigger in os.listdir('triggers'):
                command, extension = trigger.split('.')
                popenargs = [filecommands[extension], 'triggers/%s.%s' %(command,extension), data, nick, message]
                try:
                    triggerout = Popen(popenargs, stdout=PIPE).stdout.read()
                    if triggerout.strip(' ') != '':
                        privmsg(channel, triggerout)
                except:
                    print 'error'
