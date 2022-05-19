"""Handlers for system events."""

from pybotx import (
    AddedToChatEvent,
    Bot,
    ChatCreatedEvent,
    CTSLoginEvent,
    CTSLogoutEvent,
    DeletedFromChatEvent,
    IncomingMessage,
    LeftFromChatEvent,
    MentionBuilder,
)

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
async def chat_created(event: ChatCreatedEvent, bot: Bot) -> None:
    await bot.answer_message(
        body=f"Chat was created by {MentionBuilder.contact(event.creator_id)}!"
    )


@collector.added_to_chat
async def added_to_chat(event: AddedToChatEvent, bot: Bot) -> None:
    new_members = [str(MentionBuilder.contact(member)) for member in event.huids]

    await bot.answer_message(f"Hello, {', '.join(new_members)}!")


@collector.deleted_from_chat
async def deleted_from_chat(event: DeletedFromChatEvent, bot: Bot) -> None:
    if event.bot.id in event.huids:
        return

    deleted_members = [str(MentionBuilder.contact(member)) for member in event.huids]
    await bot.answer_message(f"Bye, {', '.join(deleted_members)}!")


@collector.left_from_chat
async def left_from_chat(event: LeftFromChatEvent, bot: Bot) -> None:
    if event.bot.id in event.huids:
        return

    left_members = [str(MentionBuilder.contact(member)) for member in event.huids]
    await bot.answer_message(f"{', '.join(left_members)} left our chat!")
