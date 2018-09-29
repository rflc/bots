# -*- coding: utf-8 -*-
from urllib import urlopen
from ttapi import Bot
import cleverbot
import re
import threading
import random
from random import choice
import time

AUTH   = 'ILmomQAOCHRceIlEBwAENLij'
USERID = '512034b3aaa5cd20218d181f'
#ROOMID = '5121d8f8aaa5cd20218d1da8' #Private
ROOMID = '5105bbc1aaa5cd73a44088ac' #Electronic Indie Mix

bot = Bot(AUTH, USERID, ROOMID)

autobopStat = True
cb          = cleverbot.Session()
songStat    = True
outOfGenre  = False
stage       = {}
dj          = {'name':'','id':''}
mods = []
brobot = True
queue = {}

#    global midTempo
#    lstnrs = data['listenerids']
#    for x in lstnrs:
#        if re.match('50f097bdaaa5cd4d3ca6c999', x):
#           midTempo = True
#           break;

def mssg():#Message display
    iem = ['`______ _____ ___ ` ___',
           '| ` ` ____|_` ` ` _| ` ` `\/ ` ` `|',
	   '|` ` |__` ` ` `| ` `| `| ` ` \``/ ` ` |',
	   '|` ` __| ` ` ` | ` `| `| ` `| \ / | ` `|',
           '|` ` |____`_| ` `|_| ` `| `` | ` `|',
	   '|______|______|__| ` |__|',
	   'Electronic Indie Mix']
    rck = ['.(....\............../....)',
	   '. \....\........... /..../',
	   '...\....\........../..../',
           '....\..../´¯.I.¯`\./',
	   '..../... I....I..(¯¯¯`\`',
	   '...I.....I....I...¯¯.\...\`',
	   '...I.....I´¯.I´¯.I..\...)',
	   '...\.....` ¯..¯ ´.......’',
	   '....\_________.?´',
	    'Electronic Indie Mix']
    msg = choice([iem, rck])
    for i in msg:
        time.sleep(0.1)
	bot.speak(i)
    t = threading.Timer(4000, mssg)
    t.start()

t = threading.Timer(4000, mssg)
t.start()

def enter(data):
    global mods	
    global stage
    mods = data['room']['metadata']['moderator_id']
    djs = data['room']['metadata']['djs']
    for x in djs:
        stage[x] = {'counter': 0}
    print mods

bot.on('roomChanged', enter)

def onStage(data):
    global stage
    global queue
    if  len(queue) =< 0 and !(djid in queue.values()):
	bot.remDj(djid)
    djs  = len(data['djs'])
    djid = data['user'][0]['userid']
    stage[djid] = {'counter': 0}
    if (djs > 2):
       bot.remDj()

def offStage(data):
    global stage
    djs  = len(data['djs'])
    djid = data['user'][0]['userid']
    stage.pop(djid, None)
    if (djs < 2):
       bot.addDj()

# List song stats
def stats(data):
    #song   = data['room']['metadata']['current_song']['metadata']['song']
    artist = data['room']['metadata']['current_song']['metadata']['artist']
    up     = data['room']['metadata']['upvotes']
    down   = data['room']['metadata']['downvotes']
    str    = (up, down, artist)
    bot.speak('/me %d :small_red_triangle:  %d :small_red_triangle_down: \
               for %s ' % str)

# Add song to dj counter
def djCounter(data):
    name = data['room']['metadata']['current_song']['djname'] 
    djid = data['room']['metadata']['current_song']['djid']
    djs  = data['room']['metadata']['djcount']
    global stage
    stage[djid]['counter'] += 1
    if (djs == 5):
       if (stage[djid]['counter'] >= 4):
          bot.speak('@%s the queue is now active. Thanks for your 4 spins, feel \
                     free to add yourself back to the queue' % name)
          bot.remDj(djid)

def addQueue(name, id):
    global queue
    queue[name] = id
    index = [Next, Coming up, Then, And, Plus, 6th, 7th, 8th, 9th, 10th]
    i = 0
    bot.speak('/me Queued:')
    for name in queue:
        bot.speak('/me %s %s' % (index[i], name))
        i ++

def queue():
    global queue
    index = [Next, Coming up, Then, And, Plus, 6th, 7th, 8th, 9th, 10th]
    i = 0
    bot.speak('/me Queued:')
    for name in queue:
	bot.speak('/me %s %s' % (index[i], name))
	i ++
	    
def mod(data):
    global outOfGenre
    outOfGenre = False
    global dj
    global sid
    sid        = data['room']['metadata']['current_song']['_id']
    genre      = data['room']['metadata']['current_song']['metadata']['genre']
    song       = data['room']['metadata']['current_song']['metadata']['song']
    album      = data['room']['metadata']['current_song']['metadata']['album']
    dj['name'] = data['room']['metadata']['current_song']['djname']
    dj['id']   = data['room']['metadata']['current_song']['djid']
    if (re.match('(techno|trance|dubstep|drumstep|dub|edm|idm|rap|hip.?hop|metal)',\
                genre, re.IGNORECASE) or \
       re.match('(techno|trance|dubstep|drumstep|dub|edm|idm|rap|hip.?hop|metal)',\
                song, re.IGNORECASE) or \
       re.match('(techno|trance|dubstep|drumstep|dub|edm|idm|rap|hip.?hop|metal)',\
                album, re.IGNORECASE)):
       str = (dj['name'], genre)
       bot.speak('@%s your %s song is out of genre. You have 10 seconds to skip your song\
                  or you will be escorted off the stage.' % str)
       outOfGenre = True
       t = threading.Timer(20, removeDj)
       t.start()
    return

def removeDj():
    global dj
    global outOfGenre
    if outOfGenre:
       bot.remDj(dj['id'])
    return

bot.on('newsong', mod)

def commands(data):
    global mods
    global brobot
    global dj
    global sid
    global autobopStat
    global autobopText
    global outOfGenre
    text = data['text']
    match = ''
    sender = data['senderid']
    if sender in mods:
       if re.match('adddj', text):
          bot.addDj()
       elif re.match('removedj', text):
            bot.remDj()
       elif re.match("^sleep\s?[0-9]*", text):
            match = re.match("^sleep\s?([0-9]*)", text)
            bot.roomDeregister()
            time.sleep(match)
            bot.start()
#       if re.match('kill', text)
       elif re.match('autobop', text):
           autobopStat = (False if (autobopStat is True) else True)
           if autobopStat:
               bot.pm('I\'m now autoboping', sender)
               bot.bop()
               return
           else:
               bot.pm('I\'m no longer autoboping', sender)
               return
       elif re.match('bop', text):
            bot.bop()
#       elif re.match('', text)
#       elif re.match('', text)
#       elif re.match('', text)
#       elif re.match('', text)
#       elif re.match('', text)
       elif re.match('host', text):
            ip = urlopen('http://bot.whatismyipaddress.com').read()
            bot.pm(ip, sender)
       elif re.match('\/', text):
            if outOfGenre:
               bot.pm('Moderation bypassed', sender)
               bot.speak('@%s Nevermind, you\'re ok' % dj['name'])
               outOfGenre = False
       elif re.match('songs', text):
            bot.playlistAll('default', songs)

       elif re.match('midtempo', text):
            midtempo(False) if brobot is True else midtempo(True)
       elif re.match('snag', text):
            bot.snag()
            bot.playlistAdd(sid)
            bot.pm('song added to my queue', sender)
       elif re.match('commands', text):
            autobopText = 'On' if (autobopStat is True) else 'off'
            brobotText = 'online' if (brobot is True) else 'offline'
            bot.pm('adddj -------------------------------\
                    removedj --------------------------\
                    bop ---------------------------------\
                    autobop ---------------------- %s\
                    snag -------------------------------\
           	 / ------------------- bypass mod\
           	 host --------------------------------\
           	 midtempo ------------- %s' % (autobopText, brobotText), sender)
    else:
         res = cb.Ask(text)
         bot.pm(res, sender)

bot.on('pmmed', commands)

def chat(data):
    text   = data['text']
#    sender = data['senderid'] 
    if re.match('\@?visions\s?', text):# || (sender in chatbuddies &&\
#       chatbuddies.index(sender)[count] < 3 && lastTime < now :
       res = cb.Ask(text)
       bot.speak(res)

bot.on('speak', chat)

def songs(data):
    print data

def autobop(data):
    global autobopStat
    if autobopStat:
       token = random.randrange(0, 100)
       t = threading.Timer(token, bot.bop)
       t.start()
    bot.pm('/awesome', '50f097bdaaa5cd4d3ca6c999')

bot.on('newsong', autobop)

def midtempo(status):
        global brobot
	brobot = status
	signals = {'endsong': djCounter,'endsong': stats,'add_dj':onStage, 'rem_dj': offStage}
	if status is True:
		for s, f in signals.iteritems():
		    bot.off(s, f)
        elif status is False:
                for s, f in signals.iteritems():
		    bot.on(s, f)

def knocknock(data):
    global autobopStat
    text = data['user'][0]['userid']
    if re.match('(4df63cbe4fe7d04a19002051|'
                '4df026a64fe7d063170340ea|'
                '504a5b98eb35c128770004c3|'
                '4dd89673e8a6c4624d00000d|'
                '4dd529f3e8a6c4643b000018|'
                '4e04e994a3f75175ff036e9c|'
                '4df024ba4fe7d06317031a81|'
                '4e0ab73ba3f751467d0269d1|'
                '4eeb8269590ca2576f002c17|'
                '4e540bd14fe7d02a35297102|'
                '4f0630e9590ca2315e000111|'
                '4ee08dc34fe7d0294b002b22|'
                '4f792184eb35c13ab50057d5|'
                '4e173a1ba3f751697b0eaaae|'
                '4df90d544fe7d056c0042f81|'
                '4de804a94fe7d0517b0332bf|'
                '4e330758a3f7511f1d00f019|'
                '4dfed28a4fe7d028c6023e05|'
                '4e060013a3f75175fd0a8b83|'
                '4dd5894fe8a6c47b4b000010|'
                '4df0f0144fe7d06318114ef4|'
                '4d87720baf03035235000002|'
                '4defa9eb4fe7d0012c025724|'
                '4e348c0c4fe7d03c6203abe9|'
                '4d6ed027af03036f8000000f|'
                '4e08f595a3f7517d1204e33c|'
                '4de92c5b4fe7d0517b13adf1|'
                '4dee9d454fe7d0589304d644|'
                '4dd79ea1e8a6c47847000013|'
                '4e494c59a3f75104420d7030|'
                '4e0a43eea3f7517d03122c06|'
                '4d6ed00faf03036f8000000d|'
                '4dea70c94fe7d0517b1a3519|'
                '4e0a89c4a3f751466f008329|'
                '4e3b098a4fe7d05c3206adcf|'
                '4d7af1c7af03032c7d00000b|'
                '50298547df5bcf50330562b5|'
                '4e025b334fe7d0613500e290|'
                '4df08aa54fe7d063150ac5da|'
                '4dfa5756a3f7514a2502b8e2|'
                '4d837befaf0303708f000002|'
                '4e0be6aba3f75146750e6260|'
                '4fc6fef1eb35c14ad80000ae|'
                '4de7a6ca4fe7d0348f0000c1|'
                '4f33da5ea3f75171f800490c|'
                '4ded03174fe7d00428016095|'
                '4e0889d4a3f7517d1100af78|'
                '4dd7beeae8a6c4784700002f|'
                '4de9abc74fe7d013dc026ee5|'
                '4e35e0394fe7d03c7306489b|'
                '4e1c98df4fe7d0314c0ceb52|'
                '4df0dec64fe7d063160ebc7f|'
                '4e1772c8a3f75169751156b7|'
                '4e00a51da3f75104de09be4f|'
                '4dd5af7be8a6c4208c000011|'
                '4da88a5ee8a6c47f4d000003|'
                '4df032194fe7d063190425ca|'
                '4e1b0737a3f751630903242b|'
                '4e02a72fa3f751791b02ad48|'
                '4e53dc894fe7d02a3528d739|'
                '4de68a4fe8a6c43dba000187|'
                '4f463281a3f7511c6a002850|'
                '4e18f194a3f75133bd07148a|'
                '4e1a6db9a3f75162f5018c05|'
                '4f771b67aaa5cd175d001f08|'
                '4e04f7394fe7d00b6504164b|'
                '4e78b8674fe7d045c230c8cd|'
                '4e0522bba3f75175ff05e385|'
                '4e2325494fe7d01dc7026b14|'
                '4ded4fa24fe7d00a61009f1d|'
                '4df8f9624fe7d056be037e4c|'
                '4df7a5ce4fe7d04a20077388|'
                '50c63ee3eb35c13b16811147|'
                '4df79d294fe7d04a20072b07)', text):
       autobopStat = False
       bot.pm('\/lame', '50f097bdaaa5cd4d3ca6c999')

    elif text == ('50f097bdaaa5cd4d3ca6c999'):
         midtempo(True)

bot.on('registered', knocknock)

def knockout(data):
    if data['user']['userid'] == '50f097bdaaa5cd4d3ca6c999':
       midtempo(False)

bot.on('deregistered', knockout)

bot.start()
