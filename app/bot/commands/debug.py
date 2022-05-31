from uuid import UUID

from pybotx import Bot, IncomingMessage

from app.bot.debug_messages import toggle_chat_debug
from app.bot.handler_with_help import HandlerCollectorWithHelp

collector = HandlerCollectorWithHelp()


@collector.command_with_help("/debug-toggle", description="Toggle debug mode for chat")
async def debug_toggle(message: IncomingMessage, bot: Bot) -> None:
    """`/debug-toggle chat_id`

    Send requests from chat.

    • `chat_id` - UUID of target chat.

    ```bash
    /debug-toggle 16dff275-00e1-56cd-9d8d-534a663e787f
    ```
    """
    chat_id = UUID(message.argument)
    is_enabled = toggle_chat_debug(message.chat.id, chat_id)

    if is_enabled:
        await bot.answer_message(f"Debug mode for chat `{chat_id}` is **enabled**.")
        return

    await bot.answer_message(f"Debug mode for chat `{chat_id}` is **disabled**.")
