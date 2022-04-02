import uuid
import django, os
import pathlib
import sys

sys.path.append(str(pathlib.PosixPath(os.path.abspath(__file__)).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.db import transaction
from django.conf import settings
from telegram import Bot, Update, BotCommand
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CommandHandler
from core.models import User
from bot import reply_text

def _get_bot() -> Bot:
    bot = Bot(settings.TELEGRAM_BOT_TOKEN)
    langs_with_commands = {
        'en': {
            'start': 'Start bot 🚀',
            'stop': 'Stop bot',
        },
    }
    bot.delete_my_commands()
    for language_code in langs_with_commands:
        bot.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
            ]
        )

    return bot


class TelegramBot:

    bot = _get_bot()

    @staticmethod
    def start(update: Update, context) -> None:
        with transaction.atomic():
            u, _ = User.update_or_create_user(update, context)
            u.is_stopped = False
            u.code = uuid.uuid4()
            u.save(update_fields=['is_stopped', 'code'])
            update.message.reply_text(reply_text.start(u), parse_mode='MarkdownV2')

    @staticmethod
    def stop(update: Update, context) -> None:
        u: User = User.get_user(update, context)
        if u:
            u.code = None
            u.is_stopped = True
            u.save(update_fields=['code', 'is_stopped'])
            update.message.reply_text(text='Stopped')

    @staticmethod
    def start_polling():

        updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        handler = CommandHandler('start', TelegramBot.start)
        dispatcher.add_handler(handler)

        handler = CommandHandler('stop', TelegramBot.stop)
        dispatcher.add_handler(handler)

        print("Pooling started")
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    TelegramBot.start_polling()