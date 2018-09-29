from ttapi import Bot
import re
import threading
import random

AUTH   = 'LqCxdqKkjADJZwphluPvyYFn'
USERID = '511dacd8aaa5cd4c9311ec5c'
#ROOMID = '5121d8f8aaa5cd20218d1da8'
ROOMID = '5105bbc1aaa5cd73a44088ac' #Electronic Indie Mix

autobopStat = True

bot = Bot(AUTH, USERID, ROOMID)

def songInfo(data):
    #  desc = data['description']
    # awsm = data['upvotes']
    # lm   = data['downvotes']
    # mod  = data['moderator_id']
    # djs  = data['djs']
    # dj   = data['djname']
    # meta = data['metadata']
    global sid
    sid = data['room']['metadata']['current_song']['_id']

bot.on('newsong', songInfo)

def commands(data):
    global sid
    global autobopStat
    global autobopText
    text = data['text']
    match = ''
    sender = data['senderid']
    if re.match('adddj', text):
       bot.addDj()
    elif re.match('removedj', text):
         bot.remDj()
    elif re.match("^sleep\s?[0-9]*", text):
         match = re.match("^sleep\s?([0-9]*)", text)
         bot.roomDeregister()
         time.sleep(match)
         bot.start()
#    if re.match('kill', text)
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
#    elif re.match('', text)
#    elif re.match('', text)
#    elif re.match('', text)
#    elif re.match('', text)
#    elif re.match('', text)
#    elif re.match('', text)
    elif re.match('songs', text):
         bot.playlistAll('default', songs)
#    elif re.match('', text)
    elif re.match('removesong', text):
         bot.playlistRemove('skip', 0)
    elif re.match('snag', text):
         bot.snag()
         bot.playlistAdd(sid)
         bot.pm('song added to my queue', sender)
    elif re.match('commands', text):
         autobopText = 'On' if (autobopStat is True) else 'off'
         bot.pm('songs ------------unimplemented\
                 sort ---------------unimplemented\
                 adddj -------------------------------\
                 removedj --------------------------\
                 bop ---------------------------------\
                 autobop ------------------------- %s\
                 snag ------------------------------\
                 sleep ------------unimplemented' \
                 % autobopText, sender)

bot.on('pmmed', commands)

def songs(data):
    print data

def autobop(data):
    global autobopStat
    if autobopStat:
       token = random.randrange(0, 70)
       t = threading.Timer(token, bot.bop)
       t.start()

bot.on('newsong', autobop)

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

bot.on('registered', knocknock)

bot.start()
