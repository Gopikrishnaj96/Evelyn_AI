
import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import playsound as playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.db import cursor
from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat
#playing assistant  sound function
"""@eel.expose
def playAssistantsound():
    music_dir="www\\assets\\audio\\start_sound.mp3"
     playsound(music_dir) """
def openCommand(query):
    query=query.replace(ASSISTANT_NAME, "")
    query=query.replace("open","")
    query.lower()
    

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT path FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term=extract_yt_term(query)
    speak("Playing "+search_term+"on Youtube")
    kit.playonyt(search_term)
"""
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"], sensitivities=[1, 0.7])
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index >= 0:
                 print("hotword detected")
                   # Simulate Ctrl+J
                 pyautogui.keyDown("ctrl")
                 time.sleep(0.05)
                 pyautogui.press("e")
                 time.sleep(0.05)
                 pyautogui.keyUp("ctrl")

                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

"""
#evelyn hotword detection

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Custom hotword file path
        evelyn_path = "C:/Users/USER/Desktop/jarvis/engine/evelyn_hotword.ppn"
        access_key = 'RkNLTCc6b88T3ZJWvh/3x678Jt7ZHCRWPBgM16nv0GnudZ9ZLwn4Cg=='
        
        # Load custom hotword
        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[evelyn_path],
            sensitivities=[0.9]  # You can tune this between 0.5 - 0.9
        )

        # Initialize PyAudio stream
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        print("Listening for hotword 'Evelyn'...")

        # Main loop to detect hotword
        while True:
            keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("Hotword 'Evelyn' detected!")

                # Trigger assistant (e.g., simulate Ctrl+E)
                pyautogui.keyDown("ctrl")
                time.sleep(0.05)
                pyautogui.press("e")
                time.sleep(0.05)
                pyautogui.keyUp("ctrl")

    except Exception as e:
        print("Error during hotword detection:", e)

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
# Whatsapp Message Sending
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 19
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab =13
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 11
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

