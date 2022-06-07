import datetime
from PyDictionary import PyDictionary
import os
import subprocess
import re

@staticmethod
def action_time():
    return str(datetime.datetime.now().time().strftime('%H:%M.'))

@staticmethod
def define(text):
    text = text.replace('define ','')
    if " " in text.strip():
        result = "A Term must be only a single word."
    else:
        dictionary = PyDictionary()
        result = dictionary.meaning(text.strip())
        if result:
            result = list(result.values())[0]
            result = result[0]
    return result


#Code from: https://github.com/vkorn/pyvizio#switching-channels-tvs-only
@staticmethod
def tv(text):
    print("***")
    print(text)
    print("***")

    #setup
    text = text.lower()
    auth_token = 'Zmv518ksnx'
    device_type = 'tv'
    ip = '192.168.1.2:7345'

    #see if there are any integers in string
    try:
        number = int(re.search(r'\d+', text).group())
    except:
        number = 5

    #user input parse and call

    #turning on and off
    if "turn" in text:
        if "on" in text:
            subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " power on")
            return (1)
        elif "off" in text:
            subprocess.call("pyvizio --ip="+ip+" --device_type="+device_type+" --auth="+auth_token+" power off")
            return (1)

    #volume controls
    if ("volume" in text or "turn" in text):
        if "up" in text:
            subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " volume up "+str(number))
            return (1)
        elif "down" in text:
            subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " volume down "+str(number))
            return (1)

    elif "mute" in text:
        subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " mute toggle")
        return (1)

    #changing inputs
    elif "input" in text:
        if ("smart" in text and "cast" in text) or "smartcast" in text:
            subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " input CAST")
            return (1)
        elif "retro" in text or "pie" in text:
            subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " input HDMI-2")
            return (1)
        elif "switch" in text:
            subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " input HDMI-3")
            return (1)
        elif "sapphire" in text:
            subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " input HDMI-4")
            return (1)

    #turning on apps
    elif "open" in text:
        if "netflix" in text:
            subprocess.call(
                "pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " launch-app Netflix")
            return (1)
        elif "hulu" in text:
            subprocess.call(
                "pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " launch-app Hulu")
            return (1)
        elif "youtube" in text:
            subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " launch-app YouTube")
            return (1)
        elif "disney" in text:
            subprocess.call(
                "pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " launch-app Disney+")
            return (1)
        elif "prime" in text:
            subprocess.call(
                "pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " launch-app \"Prime Video\"")
            return (1)
        elif "cast" in text:
            subprocess.call(
                "pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " launch-app \"SmartCast Home\"")
            return(1)


    return(-1)

    # subprocess.call(
    #     "pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " get-apps-list")

    # subprocess.call("pyvizio --ip=" + ip + " --device_type=" + device_type + " --auth=" + auth_token + " get-inputs-list")

    # subprocess.call("pyvizio --ip="+ip+" --device_type="+device_type+" --auth="+auth_token+" get-power-state")


