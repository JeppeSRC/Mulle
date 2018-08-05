import discord
import asyncio
import time
import threading
import json
import fileinput
from discord.voice_client import VoiceClient
from json import JSONEncoder

client = discord.Client()

jsonReloadNeeded = True
player = None
volume = 0.1
voice_channel = None
text_channel = None
audio_channel = None
leave_files = ["out1.wav", 
              "rullarut.wav"]
join_files = ["bygga.wav", "hej.wav"]

class Song(JSONEncoder):
    name = ""
    link = ""

    def __init__(self, name, link):
        self.name = name
        self.link = link


songs = [Song("gay", "Test")]

@client.event
@asyncio.coroutine
def on_ready():
    print("Bot Online!")
    global voice_channel
    global text_channel
    global audio_channel
    voice_channel = client.get_channel("338067634782208001") # DankBot 423210609752932366 Häst 338067634782208001
    text_channel = client.get_channel("338067634782208000")

    audio_channel = yield from client.join_voice_channel(voice_channel)

def checkPlayer():
    global player
    if player == None:
        return True
    else:
        if player.is_playing():
            return False
        else:
            return True

def makeString(strings, start, end):
    length = len(strings)
    result = ""

    if end == -1:
        end = len(strings)

    for i in range(start, end, 1):
        result += strings[i]
        if i != end - 1:
            result += " "

    return result

def realoadJsonFile():
    global songs
    jFile = open("songs.json", "r")

    j = json.loads(jFile.read())

    songs.clear()

    for i in range(0, len(j), 1):
        songs.append(Song(j[i]["name"], j[i]["link"]))

    jFile.close()

def writeSongsToJson():
    global songs
    jFile = open("songs.json", "w")

    jsonString = "[\n"

    for i in range(0, len(songs), 1):
        jsonString += json.dumps(songs[i].__dict__)

        if (i == len(songs)-1):
            jsonString += "\n"
        else:
            jsonString += ",\n"
    
    jsonString += "]"

    jFile.write(jsonString)
    jFile.close()

def addSong(song):
    global songs
    songs.append(song)
    writeSongsToJson()

def removeSong(name):
    global songs

    for i in songs:
        if i.name == name:
            songs.remove(i)
            writeSongsToJson()
            return True

    return False
    

realoadJsonFile()

@client.event
@asyncio.coroutine
def on_message(message):
    global player
    global volume
    global jsonReloadNeeded
    
    if message.content.lower().startswith("!mulle stop"):
        if checkPlayer() == False:
            print("player false")
            player.stop()
            yield from client.send_message(text_channel, "Ok I'll shut up")
        else:
            print("player true")
            yield from client.send_message(text_channel, "Nothing to stop you pleb!")
    if message.content.lower().startswith("!mulle fräsig kärra"):
        if checkPlayer() == False:
            return
        player = audio_channel.create_ffmpeg_player("out1.wav")
        player.start()
    elif message.content.lower().startswith("!mulle yt"):
        if checkPlayer() == False:
            return
        
        data = message.content.split(" ")

        if (len(data) < 3):
            yield from client.send_message(text_channel, "Nah bisch you need to give me ze länk")
            return

        player = yield from audio_channel.create_ytdl_player(data[2])
        player.volume = volume
        player.start()

    elif message.content.lower().startswith("!mulle ok"):
        if checkPlayer() == False:
            return
        player = audio_channel.create_ffmpeg_player("ok.wav")
        time.sleep(0.5)
        player.start()
        
    elif message.content.lower().startswith("!mulle hi"):
        if checkPlayer() == False:
            return
        player = audio_channel.create_ffmpeg_player("hi.wav")
        time.sleep(0.5)
        player.start()
    elif message.content.lower().startswith("!mulle really nigga"):
        if checkPlayer() == False:
            return
        player = audio_channel.create_ffmpeg_player("really_nigga.wav")
        time.sleep(0.5)
        player.start()
    elif message.content.lower().startswith("!mulle din mamma"):
        if checkPlayer() == False:
            return
        player = audio_channel.create_ffmpeg_player("din_mamma.wav")
        time.sleep(0.5)
        player.start()
    elif message.content.lower().startswith("!mulle backa"):
        if checkPlayer() == False:
            return
        player = audio_channel.create_ffmpeg_player("backa.mp3")
        time.sleep(0.5)
        player.start()
    elif message.content.lower().startswith("!mulle skr"):
        if checkPlayer() == False:
            return
        player = audio_channel.create_ffmpeg_player("skkkk.wav")
        time.sleep(0.5)
        player.start()
    elif message.content.lower().startswith("!mulle vol"):
        shit = message.content.split(" ")

        if len(shit) < 3:
            yield from client.send_message(text_channel, "Nigga give me ze volume")
            return

        volume = float(shit[2])

        if player != None:
            player.volume = volume
        

    elif message.content.lower().startswith("!mulle pause"):
        if player != None and not player.is_done():
            player.pause()

    elif message.content.lower().startswith("!mulle resume"):
        if player != None and not player.is_done():
            player.resume()

    elif message.content.lower().startswith("!mulle you gay"):
        yield from client.send_message(text_channel, "https://cdn.discordapp.com/attachments/323442482400722945/423542369670004756/no_u_card.jpg")

    elif message.content.lower().startswith("!mulle songs"):
        yield from client.send_message(text_channel, "Songs: ")

        shits = ""

        for i in range(0, len(songs), 1):
            shits += "%s: %s\n" % (i+1, songs[i].name)

        yield from client.send_message(text_channel, shits)

    elif message.content.lower().startswith("!mulle song "):
        name = makeString(message.content.lower().split(" "), 2, -1)
        print(name)
        
        for i in songs:
            if i.name == name:
                if player != None:
                    if not player.is_done():
                        player.stop()

                player = yield from audio_channel.create_ytdl_player(i.link)
                player.volume = volume
                player.start()
                return

        yield from client.send_message(text_channel, "Couldn't find song, stop being such a nigga")

    elif message.content.lower().startswith("!mulle add "):
        name = makeString(message.content.lower().split(" "), 3, -1)
        link = makeString(message.content.split(" "), 2, 3)

        addSong(Song(name, link))

        print("Added song \"" + name + "\"")

        yield from client.send_message(text_channel, "Added song \"" + name + "\"")

    elif message.content.lower().startswith("!mulle remove "):
        name = makeString(message.content.lower().split(" "), 2, -1)

        if (removeSong(name) == True):
            print("Removed song Name: \"" + name + "\"")

            yield from client.send_message(text_channel, "Removed song Name: \"" + name + "\"")
        else:
            yield from client.send_message(text_channel, "\"" + name + "\" isn't a song bish")

    
join_count = 0
leave_count = 0

@client.event
@asyncio.coroutine
def on_voice_state_update(before, after):
    global player
    global join_count
    global leave_count
    if not before.bot:
        if before.voice_channel == None and after.voice_channel != None:
            if player != None:
                if player.is_playing():
                    return

            player = audio_channel.create_ffmpeg_player(join_files[join_count % len(join_files)])
            join_count += 1
            time.sleep(1.25)
            player.start()
        elif before.voice_channel != None and after.voice_channel == None:
            if player != None:
                if player.is_playing():
                    return
            player = audio_channel.create_ffmpeg_player(leave_files[leave_count % len(leave_files)])
            leave_count += 1
            player.start()
        elif before.voice_channel.id != "338067634782208001" and after.voice_channel.id == "338067634782208001":
            if player != None:
                if player.is_playing():
                    return
            
            player = audio_channel.create_ffmpeg_player(join_files[join_count % len(join_files)])
            join_count += 1
            time.sleep(1.25)
            player.start()
        elif before.voice_channel.id == "338067634782208001" and after.voice_channel.id != "338067634782208001":
            if player != None:
                if player.is_playing():
                    return

            player = audio_channel.create_ffmpeg_player(leave_files[leave_count % len(leave_files)])
            leave_count += 1
            player.start()

running = True
step = 0

def update():
    while (running):
        pass

t = threading.Thread(target=update)
#t.start()

client.run("NDIzMjA2MjYxNzE5NTY0MzA4.DYnCpw.vE3PjQ5_fNG1YKasTDnKw_q58JQ")

running = False

#t.join()

print(step)