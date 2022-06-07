from typing import Any, Dict, cast

from pybotx import (
    Bot,
    BotIsNotChatMemberError,
    ChatTypes,
    IncomingMessage,
    IncomingMessageHandlerFunc,
    Mention,
    MentionBuilder,
)

from app.bot.botx_method_utils import send_json_snippet
from app.bot.datastructures import DebugSubscribers
from app.bot.formatting import pformat_json

subscribers_by_chat = DebugSubscribers()


async def debug_incoming_message_middleware(
    message: IncomingMessage, bot: Bot, call_next: IncomingMessageHandlerFunc
) -> None:
    raw_command = cast(Dict[str, Any], message.raw_command)
    for subscriber_id in subscribers_by_chat.get(message.chat.id):
        mention: Mention
        if message.chat.type == ChatTypes.PERSONAL_CHAT:
            mention = MentionBuilder.contact(message.bot.id)
        else:
            mention = MentionBuilder.chat(message.chat.id)

        try:
            await send_json_snippet(
                bot,
                message.bot.id,
                subscriber_id,
                f"Incoming request from chat {mention}:",
                pformat_json(raw_command),
                "request.json",
            )
        except BotIsNotChatMemberError:
            subscribers_by_chat.remove(subscriber_id, message.chat.id)

    await call_next(message, bot)
