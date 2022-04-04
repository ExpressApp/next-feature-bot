"""Handlers for testing special messages flags."""

from uuid import UUID

from pybotx import Bot, IncomingMessage

from app.bot.handler_with_help import HandlerCollectorWithHelp

collector = HandlerCollectorWithHelp()


@collector.command_with_help(
    "/silent-response", description="Hide next user message from history"
)
async def silent_response_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/silent-response [chat_id]`

    Send message with `silent_response` flag, which hides next user messages.
    If bot send you another message, `silent_response` flag will be reset.

    • `chat_id` - Target chat id (skip to use current chat).

    Examples:

    ```bash
    # Send message with `silent_response` to current chat:
    /silent-response

    # Send message with `silent_response`
    # to chat `123e4567-e89b-12d3-a456-426655440000`
    /silent-response 123e4567-e89b-12d3-a456-426655440000
    ```
    """

    if raw_chat_id := message.argument:
        try:
            chat_id = UUID(raw_chat_id)
        except ValueError:
            await bot.answer_message("**Error:** Invalid group chat id")
            return
    else:
        chat_id = message.chat.id

    try:
        await bot.send_message(
            bot_id=message.bot.id,
            chat_id=chat_id,
            body="Your next message will be hidden",
            silent_response=True,
        )
    except Exception as exc:
        await bot.answer_message(str(exc))
