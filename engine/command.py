import time
import pyttsx3
import speech_recognition as sr
import eel
from engine import conversation
from engine import video_audio_processing
def speak(text):
    text=str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate',174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

@eel.expose
def takecommand():
    """
    Records video with audio, extracts audio, transcribes it, and returns the video file and transcription.
    """
    print("listening....")
    eel.DisplayMessage("listening....")
    
    # Record video with audio
    video_filename = "output.mp4"
    video_audio_processing.record_video_with_audio(duration=4, output_filename=video_filename)
    print("[INFO] Recording complete.")
    # Extract audio from the video
    eel.DisplayMessage("recognizing")
    audio_filename = "output_audio.wav"
    video_audio_processing.extract_audio_from_video(video_filename, audio_filename)
    
    # Transcribe audio
    transcription = video_audio_processing.transcribe_audio_with_openai(audio_filename)
    print("[INFO] Transcribed Text:", transcription)
    # Display the transcription
    query = transcription
    eel.DisplayMessage(query)    
    # Return both the video file and the transcription
    return video_filename, query.lower()

"""text=takecommand()
speak(text)"""


@eel.expose
def allCommands(message=1):

    if message == 1:
        video_file,query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)#sends the msg to chat history
    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):
                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    _,query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)
        
        else:
           # from engine.chat.main import chatBot
           #  #it should go into conversation mode
            conversation.conversation_mode(video_file,query)

    except Exception as e:    
        print("An error occurred:", e)
        import traceback
        traceback.print_exc()  # detailed traceback    
    eel.ShowHood()




    
'''def allCommands(message=1):

    if message ==1: #message from mic
        query=takecommand()
        print(query)
        eel.senderText(query)
    else: #message from chatbox
        query=message
        eel.senderText(query)

    try:


        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)
        else:
            print("not run")
        
    except:
        print("error")
    
    eel.ShowHood()
'''
