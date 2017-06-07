# telegram bot python edition
import sys
import json
import gevent
from telegram.ext import Updater, CommandHandler


def A_test_from_bot(msg):
    with open(sys.path[0]+'/scales_bot_config', 'r') as tmp:
        config = json.loads(tmp.read())
        token, chat_id = config
    updater = Updater(token)
    updater.bot.send_message(chat_id, str(msg))


class scales_telegram_bot:
    def __init__(self, token, chat_id=None):
        self.updater = Updater(token)
        self.chat_id = chat_id
        self.updater.dispatcher.add_handler(
            CommandHandler('start', self.start)
        )

    def start(self, bot, update):
        update.message.reply_text('Hello World!')

    def _run(self, queue):
        item = queue.get()
        self.updater.bot.send_message(self.chat_id, str(item))

    def run(self, queue):
        pool = [
            gevent.spawn(self._run, queue),
            gevent.spawn(self.updater.start_polling)
        ]
        gevent.joinall(pool)


def mod_init(arg=None):
    try:
        import config
    except ImportError:
        import default_config as config
    return scales_telegram_bot(config.token, config.chat_id)


if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_socket()
    from gevent.queue import Queue
    Q = Queue()
    Q.put('hello world')
    bot = mod_init()
    bot.run(Q)
