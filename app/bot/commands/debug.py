from pybotx import Bot, IncomingMessage, Mention, MentionBuilder

from app.bot.debug_utils import (
    find_personal_chat_id_by_huid,
    get_group_chat_id_from_mentions,
)
from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.middlewares.debug_messages import subscribers_by_chat

collector = HandlerCollectorWithHelp()


@collector.command_with_help(
    "/debug-toggle", description="Toggle debug mode for a specific chat"
)
async def debug_toggle(message: IncomingMessage, bot: Bot) -> None:
    """`/debug-toggle ##chat`

    Toggle debug mode for a specific chat. All incoming and outgoing requests
    from there will be sent to the chat where this command was sent.

    • `##chat` - mention of target chat or `self` for personal chat with bot.

    ```bash
    /debug-toggle ##Chat
    /debug-toggle self
    ```
    """
    mention: Mention
    if message.argument == "self":
        chat_id = await find_personal_chat_id_by_huid(
            bot, message.bot.id, message.sender.huid
        )
        mention = MentionBuilder.contact(message.bot.id)
    else:
        chat_id = await get_group_chat_id_from_mentions(
            bot, message.bot.id, message.mentions.chats
        )
        mention = MentionBuilder.chat(chat_id)

    is_enabled = subscribers_by_chat.toggle(message.chat.id, chat_id)

    text = (
        f"Debug mode for chat {mention} is "
        f"**{'enabled' if is_enabled else 'disabled'}**."
    )

    await bot.answer_message(text)
