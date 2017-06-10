import gevent
from telegram.ext import Updater, CommandHandler


class scales_telegram_bot:
    'a telegram bot, has few function'
    # laxect.scales_bot.1.0.0
    def __init__(self, token, chat_id=None):
        self.updater = Updater(token)
        self.chat_id = chat_id
        self.updater.dispatcher.add_handler(
            CommandHandler('start', self.start)
        )

    def start(self, bot, update):
        update.message.reply_text('Hello World!')
        print(update.message.chat_id)
        # design for test.

    def _run(self, queue):
        item = queue.get()
        self.updater.bot.send_message(self.chat_id, str(item))

    def run(self, queue):
        pool = [
            gevent.spawn(self._run, queue),
            gevent.spawn(self.updater.start_polling)
        ]
        gevent.joinall(pool)


def mod_init(argv):
    token, chat_id = argv
    return scales_telegram_bot(token, chat_id)


if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_socket()
    from gevent.queue import Queue
    Q = Queue()
    Q.put('hello world')
    bot = mod_init()
    bot.run(Q)
