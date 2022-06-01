from uuid import UUID

from pybotx import Bot, IncomingMessage

from app.bot.debug_messages import subscribers_by_chat
from app.bot.handler_with_help import HandlerCollectorWithHelp

collector = HandlerCollectorWithHelp()


@collector.command_with_help(
    "/debug-toggle", description="Toggle debug mode for a specific chat"
)
async def debug_toggle(message: IncomingMessage, bot: Bot) -> None:
    """`/debug-toggle chat_id`

    Toggle debug mode for a specific chat. All incoming and outgoing requests
    from there will be sent to this chat.

    • `chat_id` - UUID of target chat.

    ```bash
    /debug-toggle 16dff275-00e1-56cd-9d8d-534a663e787f
    ```
    """
    chat_id = UUID(message.argument)
    is_enabled = subscribers_by_chat.toggle(message.chat.id, chat_id)

    text = (
        f"Debug mode for chat `{chat_id}` is "
        f"**{'enabled' if is_enabled else 'disabled'}**."
    )

    await bot.answer_message(text)
