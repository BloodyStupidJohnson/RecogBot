import speech_recognition as sr
from collections import OrderedDict
import os
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

ftkn = open('token.txt','r')
TOKEN = str(ftkn.readline())
REQUEST_KWARGS = {
    'proxy_url': 'socks5://socksproxy:telegramNeBolei@95.85.18.95:1080',
    'urllib3_proxy_kwargs': {
        'username': 'socksproxy',
        'password': 'telegramNeBolei',
    }
}
helpmessage = "/help - показывает это сообщение. Боту можно отправлять файлы в .wav формате. Пользоваться ботом можно не более 50 раз в день."
greetmessage = "Привет! Я помогу тебе узнать какое самое частое слово в твоей речи. Просто отправь мне аудиозапись своей речи в формате .wav и я начну работу."
updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 95.85.18.95:1080  login: socksproxy  password: telegramNeBolei
recognizer = sr.Recognizer()

def oggtowav():
    import librosa, soundfile
    y, sr = librosa.core.load('/home/rincewind/Загрузки/Voicebot/voice.ogg')
    soundfile.write('/home/rincewind/Загрузки/Voicebot/voice.wav', y, sr, subtype='PCM_16', endian='FILE')
# apihelper.proxy = {'http':'http://10.10.1.10:3128'}
# apihelper.proxy = {'https':'socks5://socksproxy:telegramNeBolei@95.85.18.95:1080'}

def counter(Path_to_File):
    harvard = sr.AudioFile(Path_to_File)
    with harvard as source:
        auDIO = recognizer.record(source)
    dict_of_frequent_words = OrderedDict()
    text = recognizer.recognize_google(auDIO, language="ru-RU")
    words = text.split(' ')
    words = list(map(lambda x: morph.parse(x)[0].normal_form, words))
    for i in range(len(words)):
        if words[i] in dict_of_frequent_words:
            dict_of_frequent_words[words[i]] += 1
        else:
            dict_of_frequent_words[words[i]] = 1
    vals = list(dict_of_frequent_words.values())
    similar = False
    for i in range(len(vals) - 1):
        if vals[i] == vals[i + 1]:
            similar = True
        else:
            similar = False
            break
    if similar:
        return None, text
    else:
        dict_of_frequent_words = sorted(dict_of_frequent_words.items(), key=lambda x: x[1])
        return dict_of_frequent_words, text


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=greetmessage)


def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=helpmessage)


def voi(bot, update):
    file = bot.getFile(update.message.voice.file_id)
    file.download('/home/rincewind/Загрузки/Voicebot/voice.ogg')
    oggtowav()
    result , txt = counter('/home/rincewind/Загрузки/Voicebot/voice.wav')
    if not result:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(txt))
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(txt))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-1][0]) + ' ' + str(result[-1][1]))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-2][0]) + ' ' + str(result[-2][1]))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-3][0]) + ' ' + str(result[-3][1]))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-4][0]) + ' ' + str(result[-4][1]))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-5][0]) + ' ' + str(result[-5][1]))

def aud(bot, update):
    file = bot.getFile(update.message.document.file_id)
    file.download('/home/rincewind/Загрузки/Voicebot/audio.wav')
    result, txt = counter('/home/rincewind/Загрузки/Voicebot/audio.wav')
    if not result:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(txt))
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(txt))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-1][0]) + ' ' + str(result[-1][1]))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-2][0]) + ' ' + str(result[-2][1]))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-3][0]) + ' ' + str(result[-3][1]))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-4][0]) + ' ' + str(result[-4][1]))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=str(result[-5][0]) + ' ' + str(result[-5][1]))


start_handler = telegram.ext.MessageHandler(telegram.ext.filters.Filters.voice, voi)
another_handler = telegram.ext.MessageHandler(telegram.ext.filters.Filters.document, aud)
cmdHandler1 = telegram.ext.CommandHandler('start', start)
cmdHandler2 = telegram.ext.MessageHandler('help', help)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(another_handler)
dispatcher.add_handler(cmdHandler1)
dispatcher.add_handler(cmdHandler2)
updater.start_polling()
