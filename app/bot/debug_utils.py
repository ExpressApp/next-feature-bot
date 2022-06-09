from typing import List
from uuid import UUID

from pybotx import Bot, ChatTypes, MentionChat

from app.bot.answer_error_exceptions import AnswerMessageError


async def find_personal_chat_id_by_huid(bot: Bot, bot_id: UUID, huid: UUID) -> UUID:
    for chat in await bot.list_chats(bot_id=bot_id):
        if chat.chat_type == ChatTypes.PERSONAL_CHAT and huid in chat.members:
            return chat.chat_id

    raise AnswerMessageError("**Error:** You do not have personal chat with this bot")


async def get_group_chat_id_from_mentions(
    bot: Bot, bot_id: UUID, mentions: List[MentionChat]
) -> UUID:
    if not mentions:
        raise AnswerMessageError("**Error:** Missing required arguments")

    chat_id = mentions[0].entity_id

    for chat in await bot.list_chats(bot_id=bot_id):
        if chat.chat_id == chat_id:
            return chat_id

    raise AnswerMessageError("**Error:** I am not a member of this chat")
