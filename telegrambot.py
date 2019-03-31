import logging
import requests
import datetime
import json
import copy
import os
import model


# params
TOKEN = "895504881:AAGvbrGsD8wpgsVGziVNQXgDkr0VVRxjpmg"
PORT = int(os.environ.get('PORT', '8443'))
APP_NAME = "botmanager"

from telegram.ext import Updater, MessageHandler, Filters
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

additional_input_message = "Sorry, this feature requires additional inputs."

medicial_reply = """
Your Menstrual Cycle is on time, and your next menstruation is expected to come within the next 1-3 days.  
 
You've told me that you've had mood swings lately. No worries, mood swings are normal for many women around the world. To manage your mood swings, You would want to perform relaxation exercises (e.g. deep breathing, tuning out to calming music) or get your heart pumping with a quick workout! Your mood will set to improve throughout! 
 
You seem to be struggling with managing your symptoms for cramps. For mild pains, you may apply dermal patches to manage your pain. You may also take paracetamol, doses recommended for pain if the pain is mild. If it gets too severe, you may consider switching to stronger painkillers such as Non-Steriodal Anti-Inflammatory Drugs like Naproxen to manage your pain! Let me know again, if you can manage your symptoms with these!
"""

cycle_len = 0
sym = []
state = -1
symptoms = ["acne", "backache", "bloating", "cramp","diarrhea", "dizzy", "headache", "mood", "nausea", "sore"]

def getInfo(update, args):
    username = update.message.from_user.username
    text = ' '.join(args).lower()
    if not text:
        raise ValueError('No args')
    now = datetime.datetime.now()
    return text, username, now

def createevent(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Hello. How are you?")
    bot.send_message(chat_id=update.message.chat_id, text="Tell me your cycle length.")

def handle_message(bot, update):
    global state
    global cycle_len
    text = update.message.text
    if state == -1:
        text = update.message.text
        cycle_len = int(text)
        state += 1
        bot.send_message(chat_id=update.message.chat_id, text="Tell me your " + str(symptoms[state]) +" pain level from 0 to 100.")
    elif state == 9:
        text = update.message.text
        sym.append(int(text))
        state += 1
        result = model.predict(sym,cycle_len)
        days = result["cycle_length_initial"] - result["current_day"]
        today = datetime.date.today()
        d1 = today + datetime.timedelta(days=1)
        d1str = d1.strftime("%d/%m/%Y")
        bot.send_message(chat_id=update.message.chat_id, text="According to our dataset, your next Menstrual Cycle is on " + d1str + ".")
        bot.send_message(chat_id=update.message.chat_id, text=medicial_reply)
    else:
        text = update.message.text
        sym.append(int(text))
        state += 1
        bot.send_message(chat_id=update.message.chat_id, text="Tell me your " + str(symptoms[state]) +" pain level from 0 to 100.")


def createHandler(command, handler):
    from telegram.ext import CommandHandler
    start_handler = CommandHandler(command, handler, pass_args=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=handle_message))

def main():
    createHandler('start', createevent)

    # from telegram.ext import MessageHandler, Filters
    # unknown_handler = MessageHandler(Filters.command, unknown)
    # dispatcher.add_handler(unknown_handler)


if __name__ == '__main__':
    try:
        main()
        updater.start_polling(timeout=6000)
        # if on_heroku:
        #     updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN)
        #     updater.bot.set_webhook("https://"+APP_NAME+".herokuapp.com/" + TOKEN)
        #     updater.idle()
        # else:
        #     updater.start_polling()

    except KeyboardInterrupt:
        updater.stop()
        exit()
