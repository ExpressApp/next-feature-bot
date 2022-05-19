"""Handlers for system events."""

# from pybotx import Bot, CTSLoginEvent, CTSLogoutEvent, IncomingMessage, MentionBuilder
from lalala.pybotx import Bot, CTSLoginEvent, CTSLogoutEvent, IncomingMessage, MentionBuilder, ChatCreatedEvent

from app.bot.handler_with_help import HandlerCollectorWithHelp

collector = HandlerCollectorWithHelp()


@collector.command_with_help(
    "/enable-cts-events",
    description="Enable printing cts events to current chat",
)
async def enable_cts_events(message: IncomingMessage, bot: Bot) -> None:
    """`/enable-cts-events`

    Enable printing cts events (`cts_login`, `cts_logout`) to current chat.

    This command doesn't accept arguments.
    """

    listeners = bot.state.chats_listening_cts_events
    listeners.add(message.bot.host, message.chat.id)

    await bot.answer_message("CTS events are enabled.")


@collector.command_with_help(
    "/disable-cts-events",
    description="Disable printing cts events to current chat.",
)
async def disable_cts_events(message: IncomingMessage, bot: Bot) -> None:
    """`/disable-cts-events`

    Disable printing cts events (`cts_login`, `cts_logout`) to current chat.

    This command doesn't accept arguments.
    """

    listeners = bot.state.chats_listening_cts_events
    try:
        listeners.remove(message.bot.host, message.chat.id)
    except KeyError:
        await bot.answer_message("You are not subscribed to cts events.")
        return

    await bot.answer_message("CTS events are disabled.")


@collector.cts_login
async def cts_login_handler(event: CTSLoginEvent, bot: Bot) -> None:
    listeners = bot.state.chats_listening_cts_events.get(event.bot.host)

    for chat_id in listeners:
        text = f"{MentionBuilder.contact(event.huid)} logged into {event.bot.host}"
        await bot.send_message(bot_id=event.bot.id, chat_id=chat_id, body=text)


@collector.cts_logout
async def cts_logout_handler(event: CTSLogoutEvent, bot: Bot) -> None:
    listeners = bot.state.chats_listening_cts_events.get(event.bot.host)

    for chat_id in listeners:
        text = f"{MentionBuilder.contact(event.huid)} logged out from {event.bot.host}"
        await bot.send_message(bot_id=event.bot.id, chat_id=chat_id, body=text)


@collector.chat_created
async def chat_created(_: ChatCreatedEvent, bot: Bot):
    await bot.answer_message(body="Chat created!")
