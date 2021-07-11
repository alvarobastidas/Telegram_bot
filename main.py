import constants as keys
from telegram.ext import *
import responses_2 as R


print('Bot started...')


def start_command(update, context):
    update.message.reply_text(R.start_msg)


def help_command(update, context):
    update.message.reply_text('If you need help ask google')


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.default_responses(text)

    update.message.reply_text(response)


def error(update, context):
    print(f'Udate {update} caused error {context.error}')


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()


def test_bot():
    response = 'start'
    while response != 'Operation cancelled!!':
        input_user = input('Enter your answer: ').lower()
        response = R.default_responses(input_user)
        print(response)


# main()
test_bot()