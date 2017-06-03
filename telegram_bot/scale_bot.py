import gevent
from gevent import monkey
from configparser import ConfigParser
from telegram.ext import Updater, CommandHandler
monkey.patch_socket()


def start(bot, update):
    update.message.reply_text('Hello World!')


def init(token, chat_id):
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.bot.send_message(chat_id=chat_id, text='hello world')
    updater.start_polling()


def show():
    while True:
        gevent.sleep(1)
        print('runing!')


def main():
    config = ConfigParser()
    config.read('telegram_bot_config.ini')
    gevent.joinall([
        gevent.spawn(init, config['user']['token'], config['user']['chat_id']),
        gevent.spawn(show)
    ])


if __name__ == '__main__':
    main()
