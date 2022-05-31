from typing import Any, Dict
from uuid import UUID

from pybotx import Bot, BotIsNotChatMemberError

from app.bot.datastructures import DebugSubscribers
from app.bot.formatting import pformat_json
from app.logger import logger

subscribers_by_chat = DebugSubscribers()


async def send_debug_message_for_incoming_request(
    raw_bot_message: Dict[str, Any], bot: Bot
) -> None:
    try:  # noqa: WPS:229
        chat_id = UUID(raw_bot_message["from"]["group_chat_id"])
        bot_id = UUID(raw_bot_message["bot_id"])
    except KeyError:
        logger.warning("Unable to parse incoming request for debug")
        return

    for subscriber_id in subscribers_by_chat.get_subscribers_by_chat(chat_id):
        try:
            await bot.send_message(
                bot_id=bot_id,
                chat_id=subscriber_id,
                body=f"Incoming request:\n```\n{pformat_json(raw_bot_message)}\n```",
            )
        except BotIsNotChatMemberError:
            subscribers_by_chat.toggle(subscriber_id, chat_id)
