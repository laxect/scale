import gevent
from modules import database
from telegram.ext import Updater, CommandHandler


class scales_telegram_bot:
    'a telegram bot, has few function'
    # laxect.scales_bot.2.1.1
    def __init__(self, token, chat_id=None):
        self.id = 'laxect.telegram_bot'
        self.updater = Updater(token)
        self.chat_id = chat_id
        self.db = database.database(self.id)

        self.updater.dispatcher.add_handler(
            CommandHandler('start', self.start)
        )
        self.updater.dispatcher.add_handler(
            CommandHandler('update', self.update)
        )
        self.updater.dispatcher.add_handler(
            CommandHandler('seek', self.seek)
        )
        self.updater.dispatcher.add_handler(
            CommandHandler('add', self.add)
        )

    def start(self, bot, update):
        'do something with /start'
        update.message.reply_text('Hello World!')
        print(update.message.chat_id)

    def seek(self, bot, update):
        'seek config when /seek'
        key = update.message['text'].split(' ')[1]
        update.message.reply_text(self.db.config_seek(key))

    def update(self, bot, update):
        'update config when recvive /update'
        _, key, value, *_ = update.message['text']

    def add(self, bot, update):
        'add a argv to a session'
        _, key, value, *_ = update.message['text'].split(' ')
        self.db.config_add(key, value)
        update.message.reply_text(self.db.config_seek(key))

    def _run(self, queue):
        while True:
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
