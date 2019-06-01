from selenium import webdriver
import re
import subprocess

def tokenize(text):
    text = text.split()
    tokens = []
    id=''
    for word in text:
        if re.match(r"play|search|open|and|close|how|where|what|remember|as|please|find|could you|start audio mode|start console mode|"+config["your name"], word,re.IGNORECASE):
            if not len(id) == 0:
                tokens.append(id)
                id =''
            tokens.append(word)
        else:
            if len(id) == 0:
                id+=word
            else:
                id+= " "+word
    if not len(id) == 0:
        tokens.append(id)
    return tokens

ff = None
  
proc = None

audio_mode = False

config = {}

def load_config():
    global config
    with open('config.txt') as inputfile:
      for line in inputfile:
        key = line.split("<<")
        key = [e.strip() for e in key]
        config[key[0]]=key[1]

def save_config():
    global config
    with open("config.txt","w+") as outputfile:
        for key in config:
            outputfile.write(key +" << "+ config[key]+"\n")

def change_mode(audio):
    global audio_mode
    audio_mode = audio

def get_name(name):
    if name in config:
        return config[name]
    return name

def play(name):
    global ff
    ff = webdriver.Firefox()
    ff.get("https://www.youtube.com/results?search_query="+get_name(name))
    element = ff.find_element_by_id("video-title")
    element.click()
    return ff

def search(name):
    global ff
    ff = webdriver.Firefox()
    ff.get("https://www.google.pl/search?q="+get_name(name))

def my_open(name):
    global proc
    proc = subprocess.Popen("start "+get_name(name), shell=True)

def open_website(name):
    global ff 
    ff = webdriver.Firefox()
    ff.get("https://"+get_name(name))

def close_webbrowser(name):
    global ff
    ff.close()

def close_proc(name):
    global proc
    proc.terminate()

def remember_name(key, name):
    global config
    config[key] = name

def con_repeat(name, instruct):
    if re.match(r"and",name):
        parse(" ".join(instruct))
    else:
        parse(name+" "+" ".join(instruct))

def parse(text,call_name = False):
    instruct = tokenize(text)
    instruct = list(filter(lambda x: not re.match(r"please|could you|find|tell me",x), instruct))

    if len(instruct) and  (not call_name or re.match(r""+config["your name"],instruct.pop(0),re.IGNORECASE)):
        instruction = instruct.pop(0)
        if re.match(r"play",instruction):
            play(instruct.pop(0))
            if(len(instruct)):
                con_repeat(instruct.pop(0),instruct)
        elif re.match(r"open",instruction):
            sec = instruct.pop(0)
            if re.match(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",get_name(sec)):
                open_website(sec)
                if(len(instruct)):
                    con_repeat(instruct.pop(0),instruct)
            else:
                my_open(sec)
                if(len(instruct)):
                    con_repeat(instruct.pop(0),instruct)
        elif re.match(r"search",instruction):
            search(instruct.pop(0))
            if(len(instruct)):
                con_repeat(instruct.pop(0),instruct)
        elif re.match(r"close",instruction):
            sec = instruct.pop(0)
            if re.match(r"browser",sec):
                close_webbrowser(sec)
                if(len(instruct)):    
                    con_repeat(instruct.pop(0),instruct)
            else:
                close_proc(sec)
                if(len(instruct)):
                    con_repeat(instruct.pop(0),instruct)
        elif re.match(r"how|where|what",instruction):
            search(instruction + " " + instruct.pop(0))
            if(len(instruct)):
                con_repeat(instruct.pop(0),instruct)
        elif re.match(r"remember",instruction):
            word = instruct.pop(0)
            as_ = instruct.pop(0)
            remember_name(instruct.pop(0),word)
            save_config()
            if(len(instruct)):    
                con_repeat(instruct.pop(0),instruct)
        elif re.match(r"start audio mode",instruction):
            change_mode(True)
            if(len(instruct)):    
                con_repeat(instruct.pop(0),instruct)
        elif re.match(r"start console mode",instruction):
            change_mode(False)
            if(len(instruct)):    
                con_repeat(instruct.pop(0),instruct)
        else:
            print("Sorry I don't understand this command")
