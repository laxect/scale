from modules import database
from telegram.ext import Updater, CommandHandler
from . import stand_task


class scales_telegram_bot(stand_task.service):
    'a telegram bot, has few function'
    def __init__(self, token, chat_id=None):
        super().__init__()
        self.id = 'laxect.telegram_bot'
        self.version = 2
        self.inbox = 'inbox'
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

    def _msg_handle(self, msg):
        if self.debug:
            msg = f'A message received:\n{str(msg)}'
            self.debug_information_format(msg)
            return
        self.updater.bot.send_message(self.chat_id, str(msg))

    def _run(self, mail_service=None, targets=None):
        if self.debug:
            return
        self.updater.start_polling()


def mod_init(argv):
    token, chat_id = argv
    return scales_telegram_bot(token, chat_id)
