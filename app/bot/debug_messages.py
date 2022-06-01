from pybotx import (
    Bot,
    BotIsNotChatMemberError,
    IncomingMessage,
    IncomingMessageHandlerFunc,
)

from app.bot.botx_method_utils import send_json_snippet
from app.bot.datastructures import DebugSubscribers
from app.bot.formatting import pformat_json

subscribers_by_chat = DebugSubscribers()


async def debug_incoming_message_middleware(
    message: IncomingMessage, bot: Bot, call_next: IncomingMessageHandlerFunc
) -> None:
    for subscriber_id in subscribers_by_chat.get(message.chat.id):
        try:
            await send_json_snippet(
                bot,
                "Incoming request:",
                pformat_json(message.raw_command),
                "request.json",
                bot_id=message.bot.id,
                recipient=subscriber_id,
            )
        except BotIsNotChatMemberError:
            subscribers_by_chat.remove(subscriber_id, message.chat.id)

    await call_next(message, bot)
