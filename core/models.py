from typing import Dict
from django.db import models
from typing import Union, Optional, Tuple

from django.db import models
from django.db.models import QuerySet
from telegram import Update
from telegram.ext import CallbackContext


def extract_user_data_from_update(update: Update) -> Dict:
    """ python-telegram-bot's Update instance --> User info """
    if update.message is not None:
        user = update.message.from_user.to_dict()
    elif update.inline_query is not None:
        user = update.inline_query.from_user.to_dict()
    elif update.chosen_inline_result is not None:
        user = update.chosen_inline_result.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.from_user is not None:
        user = update.callback_query.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.message is not None:
        user = update.callback_query.message.chat.to_dict()
    else:
        raise Exception(f"Can't extract user data from update: {update}")

    return dict(
        user_id=user["id"],
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name", "language_code"]
            if k in user and user[k] is not None
        },
    )


class User(models.Model):

    code = models.CharField(max_length=124, unique=True, blank=True, null=True, default=None)
    user_id = models.PositiveBigIntegerField(primary_key=True)  # chat_id

    username = models.CharField(max_length=32, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True, default=None)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", blank=True, null=True, default=None)
    deep_link = models.CharField(max_length=64, blank=True, null=True, default=None)

    is_stopped = models.BooleanField(default=False)

    @classmethod
    def update_or_create_user(cls, update: Update, context: CallbackContext):
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if created:
            # Save deep_link to User model
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext):
        data = extract_user_data_from_update(update)
        return User.objects.filter(user_id=data["user_id"]).first()

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]):
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"

