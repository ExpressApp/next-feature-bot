"""Configuration for bot instance."""

from app.bot.bot_with_help import BotWithHelp
from app.bot.commands import (
    administration,
    botx_callback_method,
    botx_method,
    common,
    credentials,
    edit,
    events,
    files,
    markup,
    mentions,
    search,
    spam,
    special_messages,
)
from app.bot.error_handlers.internal_error import internal_error_handler
from app.settings import settings

bot = BotWithHelp(
    collectors=[
        administration.collector,
        botx_callback_method.collector,
        botx_method.collector,
        common.collector,
        credentials.collector,
        edit.collector,
        events.collector,
        files.collector,
        markup.collector,
        mentions.collector,
        search.collector,
        spam.collector,
        special_messages.collector,
    ],
    bot_accounts=settings.BOT_CREDENTIALS,
    exception_handlers={Exception: internal_error_handler},
)
