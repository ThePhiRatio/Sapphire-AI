# for speech-to-text
import speech_recognition as sr

# for text-to-speech
from gtts import gTTS

# for language model
import transformers

# for data
import os
import timeit
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import vlc
import threading

#for functions
from functions import *

# for texting
from texting import *

#Show input devices
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f'{index}, {name}')

#Guide From: https://www.analyticsvidhya.com/blog/2021/10/complete-guide-to-build-your-ai-chatbot-with-nlp-in-python/

# Building the AI

class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = False
        recognizer.pause_threshold = 0.8
        recognizer.phrase_time_limit = 8
        # with sr.Microphone(device_index=3) as mic:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.1)
            print("Listening...")
            starttime1 = timeit.default_timer()
            # audio = recognizer.listen(mic)
            audio = recognizer.record(mic, duration=5)
            endtime1 = timeit.default_timer()
            print("Audio Time = ", (endtime1 - starttime1))
            self.text="ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")

    @staticmethod
    def text_to_speech(text):
        if text == "":
            print("ERROR")
        else:
            print((ai.name+" --> "), text)
            speaker = gTTS(text=text, lang="en", slow=False)
            speaker.save("res.mp3")

            vlc_instance = vlc.Instance("--no-video")
            player = vlc_instance.media_player_new()

            media = vlc_instance.media_new("res.mp3")

            player.set_media(media)
            player.play()


    def wake_up(self, text):
        return True if (self.name).lower() in text.lower() else False


#Add functions here
def parse_input(txt):
    ## action time
    txt = txt.lower()
    if "time" in txt and "is" in txt and "it" in txt:
        res = action_time()
    elif "tv" in txt or "franklin" in txt:
        val = tv(txt)
        if val == -1:
            res = "TV Command is not recognized."
        if val == 1:
            res = "TV Command Recognized."
    elif "define" in txt:
        res = define(txt)
    elif ai.name.lower() in txt.lower():
        res = np.random.choice(
            ["That's me!, Sapphire!", "Hello I am Sapphire the AI", "Yes I am Sapphire!", "My name is Sapphire, okay?!", "I am Sapphire and I am alive!",
             "It's-a Me!, Sapphire!"])
    ## respond politely
    elif any(i in txt for i in ["thank", "thanks"]):
        res = np.random.choice(
            ["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!",
             "mention not."])
    # elif any(i in txt for i in ["exit", "close"]):
    #     res = np.random.choice(
    #         ["Tata!", "Have a good day!", "Bye!", "Goodbye!", "Hope to meet soon!", "peace out!"])
    #     ex = False
    ## conversation
    else:
        if txt == "ERROR":
            # res="Sorry, come again?"
            res = ""
        if txt == "":
            res = ""
        if txt == None:
            res = ""
        else:
            starttime1 = timeit.default_timer()
            chat = nlp(transformers.Conversation(txt), pad_token_id=50256)
            endtime1 = timeit.default_timer()
            print("Transformer Time = ", (endtime1 - starttime1))
            res = str(chat)
            res = res[res.find("bot >> ") + 6:].strip()
    return res


#Create AI here so both of the
ai = ChatBot(name="Sapphire")
nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
os.environ["TOKENIZERS_PARALLELISM"] = "true"

def sapphire():
    ex = True
    start = 0
    while ex:
        starttime1 = timeit.default_timer()
        ai.speech_to_text()
        endtime1 = timeit.default_timer()
        print("speech_to_text() Time = ", (endtime1 - starttime1))
        ## wake up
        if ai.wake_up(ai.text) is True:
            #remove Sapphire from phrase
            if ai.text != "Sapphire":
                ai.text = ai.text.lower().replace(ai.name.lower(), "", 1)
            res = parse_input(ai.text)
            # if start == 0:
            #     res = "Hello I am Sapphire the AI, what can I do for you?"
            #     start = 1
            # else:
            #     res = parse_input(ai.text)
            ai.text_to_speech(res+'.')
        # try:
        if has_email():
            email_results = read_email(Delete_Mails=True)
            for i in range(len(email_results)):
                print("Email Results:")
                print(email_results[i])
                res = parse_input(email_results[i][0])
                print((ai.name + " --> "), res)
                send_sms_via_email(email_results[i][1], str(res), email_results[i][2])
        # except:
        #     pass

# def sapphire_email():
#     ex = True
#     while ex:
#         if has_email():
#             email_results = read_email()
#             for i in range(len(email_results)):
#                 print("Email Results:")
#                 print(email_results[i])
#                 res = parse_input(email_results[i][0])
#                 print((ai.name + " --> "), res)
#                 send_sms_via_email(email_results[i][1], str(res), email_results[i][2])


# Running the AI
if __name__ == "__main__":

    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    # sapphire_email()
    sapphire()
    # threading.Thread(target=sapphire_email).start()
    # threading.Thread(target=sapphire_audio).start()
