#BEREZA ALFA 0.1

import bereza_config
import os, webbrowser, sys
from num2words import num2words
from datetime import datetime
import bereza_speak
import bereza_recognition
from fuzzywuzzy import fuzz
import alsaaudio

print('Bereza ( ALFA 0.1 ) start work')

def first_clean(voice):
    voice = voice.replace('{', '')
    voice = voice.replace('"text"', '')
    voice = voice.replace(':', '')
    voice = voice.replace('}', '')
    voice = voice.replace('    ', '')
    voice = voice.replace('"', '')
    return voice

def find_name(voice: str):
    for x in voice.split():
        if x in bereza_config.NAME:
            return True
    return False

def ber_respond(voice) -> None:
    voice = first_clean(voice)
    if find_name(voice):
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in bereza_config.CMDS.keys():
            bereza_speak.speaking('Что')
        else:
            execute_cmd(cmd['cmd'])

def filter_cmd(raw_voice: str) -> str:
    cmd = raw_voice
    for x in bereza_config.NAME:
        cmd = cmd.replace(x, '')
    for x in bereza_config.WORDSTOACTIVE:
        cmd = cmd.replace(x, '').strip()

    return cmd

def recognize_cmd(cmd: str) -> dict:
    rc = {'cmd': '', 'percent': 0}
    for c, v in bereza_config.CMDS.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc

def execute_cmd(cmd: str) -> None:
    if cmd == 'help':
        bereza_speak.speaking('я умею открывать ютуб, говорить время, а также менять громкость устройства')
    elif cmd == 'youtube':
        webbrowser.open('https://www.youtube.com', new=2)
    elif cmd == 'wtime':
        currenttime = datetime.now()
        bereza_speak.speaking(num2words(currenttime.hour, lang='ru') + ' часов ' + num2words(currenttime.minute, lang='ru') + ' минут')
    elif cmd == 'upvolume':
        bereza_speak.speaking('повысила громкость на десять')
        vol = alsaaudio.Mixer()
        if vol.getvolume()[0] < 90:
            vol.setvolume(vol.getvolume()[0] + 10)
        else:
            vol.setvolume(100)
    elif cmd == 'downvolume':
        bereza_speak.speaking('понизила громкость на десять')
        vol = alsaaudio.Mixer()
        if vol.getvolume()[0] > 10:
            vol.setvolume(vol.getvolume()[0] - 10)
        else:
            vol.setvolume(0)



bereza_recognition.listen(ber_respond)
