"""Configuration for bot instance."""

from httpx import AsyncClient

from app.bot.bot_with_help import BotWithHelp
from app.bot.commands import (
    administration,
    botx_callback_method,
    botx_method,
    common,
    credentials,
    debug,
    edit,
    events,
    files,
    internal_bot_notification,
    markup,
    mentions,
    search,
    spam,
    special_messages,
)
from app.bot.error_handlers.internal_error import internal_error_handler
from app.bot.middlewares.answer_error_message import answer_error_middleware
from app.bot.middlewares.debug_messages import debug_incoming_message_middleware
from app.settings import settings

bot = BotWithHelp(
    httpx_client=AsyncClient(
        verify=settings.CUSTOM_CA_CERT_PATH or True,  # custom or default
        cert=settings.CUSTOM_CLIENT_CERT_PATH or None,  # type: ignore
    ),
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
        internal_bot_notification.collector,
        debug.collector,
    ],
    bot_accounts=settings.BOT_CREDENTIALS,
    exception_handlers={Exception: internal_error_handler},
    middlewares=[debug_incoming_message_middleware, answer_error_middleware],
)
