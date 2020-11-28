from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Updater, Dispatcher, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
import wikipedia
import requests

bot = Bot("1425886079:AAGelsCvLXwJs-S7Psz9uOHIG4dXBIHwd4k")

print(bot.get_me())

updater = Updater("1425886079:AAGelsCvLXwJs-S7Psz9uOHIG4dXBIHwd4k", use_context=True)

dispatcher: Dispatcher = updater.dispatcher

keyword = ''
chat_id = ''


def initial(update: Update, context: CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Welcome, you can search for any information or image here',
        parse_mode=ParseMode.HTML

    )


def displaykeyboard(update: Update, context: CallbackContext):
    global keyword, chat_id

    keyword = update.message.text
    chat_id = update.message.chat_id

    keyboard = [[
        InlineKeyboardButton('INFO', callback_data="INFO"),
        InlineKeyboardButton('IMAGE', callback_data='IMAGE')
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please select:', reply_markup=reply_markup)


def clickoption(update: Update, context: CallbackContext):
    global keyword, chat_id

    query: CallbackQuery = update.callback_query

    if query.data == "INFO":
        summary = wikipedia.summary(keyword)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=summary,
            parse_mode=ParseMode.HTML

        )
    if query.data == "IMAGE":
        headers = {'apikey': 'f1727fb0-3117-11eb-9ecc-7faf5c463e2c'}

        params = (
            ("q", keyword),
            ("tbm", "isch"),
        )

        response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)

        print(response)

        data = response.json()
        first_image = data['image_results'][0]['thumbnail']
        print(first_image)

        bot.send_photo(chat_id=chat_id, photo=first_image)


dispatcher.add_handler(MessageHandler(Filters.text, displaykeyboard))
dispatcher.add_handler(CallbackQueryHandler(clickoption))
updater.start_polling()
