from typing import Any, Dict, Set
from uuid import UUID

from pybotx import Bot

from app.bot.formatting import pformat_json

subscribers_by_chat: Dict[UUID, Set[UUID]] = {}


def toggle_chat_debug(subscriber_id: UUID, chat_id: UUID) -> bool:
    if chat_id not in subscribers_by_chat:
        subscribers_by_chat[chat_id] = {subscriber_id}
        return True

    if subscriber_id not in subscribers_by_chat[chat_id]:
        subscribers_by_chat[chat_id].add(subscriber_id)
        return True

    subscribers_by_chat[chat_id].remove(subscriber_id)
    return False


def delete_chat_from_debug(chat_id: str) -> None:
    subscribers_by_chat.pop(UUID(chat_id))


async def send_debug_message_for_incoming_request(
    raw_bot_message: Dict[str, Any], bot: Bot
) -> None:
    chat_id = UUID(raw_bot_message["from"]["group_chat_id"])
    if chat_id not in subscribers_by_chat:
        return

    bot_id = UUID(raw_bot_message["bot_id"])
    for subscriber_id in subscribers_by_chat[chat_id]:
        await bot.send_message(
            bot_id=bot_id,
            chat_id=subscriber_id,
            body=f"Incoming request:\n```\n{pformat_json(raw_bot_message)}\n```",
        )
