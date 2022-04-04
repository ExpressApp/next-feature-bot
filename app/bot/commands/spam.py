"""Sending multiple messages."""

import asyncio
from typing import Any, Awaitable

from pybotx import Bot, IncomingMessage

from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.regular_expressions import SPAM_ARGS_REGEXP

collector = HandlerCollectorWithHelp()


async def delay_start(coro: Awaitable[Any], delay: float) -> Any:
    await asyncio.sleep(delay)
    return await coro


@collector.command_with_help(
    "/spam", description="Send multiple messages with optional delay"
)
async def send_spam(message: IncomingMessage, bot: Bot) -> None:
    """`/spam quantity [delay]`

    Send multiple messages with optional delay.

    • `quantity` - Number of messages to send.
    • `delay` - Delay between messages sending.

    Examples:

    ```bash
    # Send 5 messages without delay
    /spam 5

    # Send 3 messages with 1 second delay
    /spam 3 1
    ```
    """

    if not (match := SPAM_ARGS_REGEXP.search(message.argument)):
        await bot.answer_message("**Error:** Invalid arguments")
        return

    quantity = int(match.group("quantity"))
    delay = int(raw_delay) if (raw_delay := match.group("delay")) else 0

    tasks = [
        delay_start(
            bot.answer_message(f"Spam {task_number}"),
            delay * task_number,
        )
        for task_number in range(quantity)
    ]

    await asyncio.gather(*tasks)
