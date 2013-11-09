bum
=

bum is a simple IRC bot written in Python 2.7 that is inspired by [sadbot](https://github.com/doidbb/sadbot). It is in very early development stages.

The name comes from the following train of thought: 

bot => butt sounds like bot => bum is a synonym of butt (butt was taken)

Also bum.py looks like bumpy.

Features
=
* __Multi-language__ modules and triggers
* Single-server action (use another instance of the bot for a different server)
* Logging both others and self
* Easy to use and make modules
* Small and simple

Configuration
=
* The configuration file is the bot itself, bum.py.
* Change network, botnick, channels and password to your own values in bum.py.
* Optionally edit the prefixes. Please don't use prefixes that take up more than 1 byte in Python, they just don't work yet.
* Add or edit the filecommands dictionary depending on what command you want to use for certain module file extensions.
* Run bum.py

Module and trigger "API"
=
Modules
-
* Modules and triggers can be in any language. Just make sure the file extension and program are in the filecommands directory.
* Modules should be put in the "modules/" directory.
* The commands for the modules are their filenames without the extensions. 
* The first argument(argv[1]) is the raw IRC data, (:name!~nick@vhost PRIVMSG #channel :>command arguments).
* The second argument(argv[2]) is the nick of the person who executed the command.
* The rest of the arguments are arguments for the command. Use ' '.join(argv[3:]) if you want to get a sentence from the arguments.
* If you want to have the output use /me or ACTION, add [me] in the beginning of the output. (example in modules/beer.py)
* The output for the module should be printed, so you receive the same output as you would if you executed the module in a terminal.
* The output can be multiple lines. 

Triggers
-
* Triggers should be put in the "triggers/" directory.
* Every file in the directory is executed whenever something is said. 
* The arguments and the output are the same as on the modules.

Examples
=
Module example:

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    # what this module does
    from sys import argv
    
    channel = argv[1].split()[2]
    nick = argv[2]
    message = ' '.join(argv[3:])
    
    print 'Your name is %s.' %nick
    print 'You are in the channel %s.' %channel
    print 'You just said "%s".' %message
    print 'You are 9 years old.'

Trigger example:

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    # what this trigger does
    from sys import argv
    
    message = ' '.join(argv[3:])

    if 'boobs' in message:
        print 'Ha! You said boobs.'

Conversation example:

    <andri> My hovercraft is full of eels
    <andri> s/[aeiuy]/o/g
    <bum> <andri> Mo hovorcroft os foll of ools
    <andri> I am a
    <andri> s/$/ noob
    <bum> <andri> I am a noob
    <andri> !rustle
    <bum> That really expressed my sweeties.
    <Drooid> Hey guys how to I install gentoo?
    <andri> :lmddgtfy how to install gentoo
    <bum> https://lmddgtfy.net/?q=how%20to%20install%20gentoo
    <andri> >quote andri
    <bum> 2013-11-02 <andri> thanks doge
    <andri> I AM SHOUTING FOR NO REASON
    <bum> MY HOVERCRAFT IS FULL OF EELS

TODO
=
* __DOCUMENTATION__
* Fix current modules
* More modules: __help__, url titles, dictionary, python, remind, tell, translate, urban dictionary, wikipedia, search engine, wolfram alpha, more fun modules
* Modules in other languages to prove that they do work
* A greeting feature
* _Maybe_ a better way to make simple triggers
* ~~If possible, make it a little faster~~
* A way for modules to be able to kick
* Fix bugs
* Come up with clever examples
