"""Handlers for testing administration methods."""

from uuid import UUID

from pybotx import (
    Bot,
    CantUpdatePersonalChatError,
    ChatCreationError,
    ChatCreationProhibitedError,
    ChatNotFoundError,
    ChatTypes,
    IncomingMessage,
    InvalidUsersListError,
    Mention,
    PermissionDeniedError,
    StealthModeDisabledError,
)

from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.mentions import user_mentions_without_bot
from app.bot.regular_expressions import (
    CREATE_CHAT_ARGS_REGEXP,
    ENABLE_STEALTH_MODE_ARGS_REGEXP,
)

collector = HandlerCollectorWithHelp()


@collector.command_with_help(
    "/enable-stealth-mode",
    description="Enable stealth mode in target chat",
)
async def enable_stealth(
    message: IncomingMessage,
    bot: Bot,
) -> None:
    """`/enable-stealth-mode burn_in expire_in [disable_web] [chat_id]`

    Enable stealth mode in target chat.

    • `burn_in` - Time to live after reading.
    • `expire_in` - Time to live after sending.
    • `disable_web` - Messages will be shown in web-client.
    • `chat_id` - Target chat id (skip to use current chat).

    Examples:

    ```bash
    # Enable stealth mode (messages available during 10 minutes after reading
    # and 60 minutes after sending, also available in web-client)
    /enable-stealth-mode 10 60 disable_web

    # Enable stealth mode with same settings
    # in chat `123e4567-e89b-12d3-a456-426655440000`
    /enable-stealth-mode 10 60 disable_web 123e4567-e89b-12d3-a456-426655440000
    ```
    """

    if not (match := ENABLE_STEALTH_MODE_ARGS_REGEXP.search(message.argument)):
        await bot.answer_message("**Error:** Missing required arguments")
        return

    burn_in = int(match.group("burn_in"))
    expire_in = int(match.group("expire_in"))
    disable_web = bool(match.group("disable_web"))

    if match.group("chat_id"):
        try:
            chat_id = UUID(match.group("chat_id"))
        except ValueError:
            await bot.answer_message("**Error:** Invalid group chat id")
            return
    else:
        chat_id = message.chat.id

    await bot.enable_stealth(
        chat_id=chat_id,
        bot_id=message.bot.id,
        ttl_after_read=burn_in,
        total_ttl=expire_in,
        disable_web_client=disable_web,
    )

    await bot.answer_message("Stealth mode enabled")


@collector.command_with_help(
    "/disable-stealth-mode",
    description="Disable stealth mode in target chat",
)
async def disable_stealth(message: IncomingMessage, bot: Bot) -> None:
    """`/disable-stealth-mode [chat_id]`

    Disable stealth mode in target chat.

    • `chat_id` - Target chat id (skip to use current chat).

    Examples:

    ```bash
    # Disable stealth mode in current chat
    /disable-stealth-mode

    # Disable stealth mode in chat `123e4567-e89b-12d3-a456-426655440000`
    /disable-stealth-mode 123e4567-e89b-12d3-a456-426655440000
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
        await bot.disable_stealth(
            chat_id=chat_id,
            bot_id=message.bot.id,
        )
    except StealthModeDisabledError as exc:
        await bot.answer_message(str(exc))
        return

    await bot.answer_message("Stealth mode disabled")


@collector.command_with_help(
    "/add-users",
    description="Add users to target chat by mentions",
)
async def add_users_to_chat(message: IncomingMessage, bot: Bot) -> None:
    """`/add-users [chat_id] user_mentions...`

    Add users to target chat by mentions.

    • `chat_id` - Target chat id (skip to use current chat).
    • `user_mentions...` - User mentions. Could be specified in any position.

    Examples:

    ```bash
    # Add user `@@User 1` to current chat
    /add-users @@User 1

    # Add users `@User 1` and `@@User 2`
    # to chat `123e4567-e89b-12d3-a456-426655440000`
    /add-users @User 1 @@User 2 123e4567-e89b-12d3-a456-426655440000
    """

    user_mentions = user_mentions_without_bot(message)
    if not user_mentions:
        await bot.answer_message("**Error:** Missing required arguments")
        return

    if raw_chat_id := message.argument:
        try:
            chat_id = UUID(raw_chat_id)
        except ValueError:
            await bot.answer_message("**Error:** Invalid group chat id")
            return
    else:
        chat_id = message.chat.id

    try:
        await bot.add_users_to_chat(
            bot_id=message.bot.id,
            chat_id=chat_id,  # TODO: Split mentions in several classes in pybotx
            huids=[user.entity_id for user in user_mentions],  # type: ignore
        )
    except (ChatNotFoundError, PermissionDeniedError) as exc:
        await bot.answer_message(str(exc))
        return

    await bot.answer_message("Users were added into chat")


@collector.command_with_help(
    "/remove-users",
    description="Remove users from target chat by contact mentions",
)
async def remove_users_from_chat(message: IncomingMessage, bot: Bot) -> None:
    """`/remove-users [chat_id] user_mentions...`

    Remove users from target chat by mentions.

    • `chat_id` - Target chat id (skip to use current chat).
    • `user_mentions...` - User mentions. Could be specified in any position.

    Examples:

    ```bash
    # Remove user `@@User 1` from current chat
    /remove-users @@User 1

    # Remove users `@User 1` and `@@User 2`
    # from chat `123e4567-e89b-12d3-a456-426655440000`
    /remove-users @User 1 @@User 2 123e4567-e89b-12d3-a456-426655440000
    """

    user_mentions = user_mentions_without_bot(message)
    if not user_mentions:
        await bot.answer_message("**Error:** Missing required arguments")
        return

    if raw_chat_id := message.argument:
        try:
            chat_id = UUID(raw_chat_id)
        except ValueError:
            await bot.answer_message("**Error:** Invalid group chat id")
            return
    else:
        chat_id = message.chat.id

    try:
        await bot.remove_users_from_chat(
            bot_id=message.bot.id,
            chat_id=chat_id,
            huids=[user.entity_id for user in user_mentions],  # type: ignore
        )
    except (ChatNotFoundError, PermissionDeniedError) as exc:
        await bot.answer_message(str(exc))
        return

    await bot.answer_message("Users were removed from chat")


@collector.command_with_help(
    "/promote-to-chat-admins",
    description="Promote users to admins in target chat by contact mentions",
)
async def promote_to_chat_admin(message: IncomingMessage, bot: Bot) -> None:
    """`/promote-to-chat-admins [chat_id] user_mentions...`

    Promote users to admins in target chat by mentions.

    • `chat_id` - Target chat id (skip to use current chat).
    • `@@user...` - User mentions. Could be specified in any position.

    Examples:

    ```bash
    # Promote user `@@User 1` to admin in current chat
    /promote-to-chat-admins @@User 1

    # Promote users `@User 1` and `@@User 2` to admins
    # in chat `123e4567-e89b-12d3-a456-426655440000`
    /promote-to-chat-admins @User 1 @@User 2 123e4567-e89b-12d3-a456-426655440000
    """

    user_mentions = user_mentions_without_bot(message)
    if not user_mentions:
        await bot.answer_message("**Error:** Missing required arguments")
        return

    if raw_chat_id := message.argument:
        try:
            chat_id = UUID(raw_chat_id)
        except ValueError:
            await bot.answer_message("**Error:** Invalid group chat id")
            return
    else:
        chat_id = message.chat.id

    try:
        await bot.promote_to_chat_admins(
            bot_id=message.bot.id,
            chat_id=chat_id,
            huids=[user.entity_id for user in user_mentions],  # type: ignore
        )
    except (
        ChatNotFoundError,
        PermissionDeniedError,
        CantUpdatePersonalChatError,
        InvalidUsersListError,
    ) as exc:
        await bot.answer_message(str(exc))
        return

    await bot.answer_message("Users were promoted to admins")


@collector.command_with_help(
    "/pin-message",
    description="Pin message in target chat",
)
async def pin_message(message: IncomingMessage, bot: Bot) -> None:
    """`/pin-message message_id [chat_id]`

    Pin message in target chat.

    • `message_id` - Message id to pin.
    • `chat_id` - Target chat id (skip to use current chat).

    Examples:

    ```bash
    # Pin message with id `123e4567-e89b-12d3-a456-426655440000`
    # in current chat
    /pin-message 123e4567-e89b-12d3-a456-426655440000

    # Pin message with id `123e4567-e89b-12d3-a456-426655440000`
    # in chat `277a1903-f0f1-44f1-ab1d-1af33d2c81f2`
    /pin-message 123e4567-e89b-12d3-a456-426655440000 277a1903-f0f1-44f1-ab1d-1af33d2c81f2
    ```
    """

    if not message.arguments:
        await bot.answer_message("**Error:** Missing required arguments")
        return

    try:
        message_id = UUID(message.arguments[0])
    except ValueError:
        await bot.answer_message("**Error:** Message ID is invalid")
        return

    try:
        chat_id = UUID(message.arguments[1])
    except IndexError:
        chat_id = message.chat.id
    except ValueError:
        await bot.answer_message("**Error:** Chat ID is invalid")
        return

    try:
        await bot.pin_message(
            bot_id=message.bot.id,
            chat_id=chat_id,
            sync_id=message_id,
        )
    except (PermissionDeniedError, ChatNotFoundError) as exc:
        await bot.answer_message(str(exc))
        return

    await bot.answer_message("Message was pinned")


@collector.command_with_help(
    "/unpin-message",
    description="Unpin message in target chat",
)
async def unpin_message(message: IncomingMessage, bot: Bot) -> None:
    """`/unpin-message [chat_id]`

    Unpin message in target chat.

    • `chat_id` - Target chat id (skip to use current chat).

    Examples:

    ```bash
    # Unpin message in current chat
    /unpin-message

    # Unpin message in chat `277a1903-f0f1-44f1-ab1d-1af33d2c81f2`
    /unpin-message 277a1903-f0f1-44f1-ab1d-1af33d2c81f2
    ```
    """

    if raw_chat_id := message.argument:
        try:
            chat_id = UUID(raw_chat_id)
        except ValueError:
            await bot.answer_message("**Error:** Chat ID is invalid")
            return
    else:
        chat_id = message.chat.id

    try:
        await bot.unpin_message(
            bot_id=message.bot.id,
            chat_id=chat_id,
        )
    except (ChatNotFoundError, PermissionDeniedError) as exc:
        await bot.answer_message(str(exc))
        return

    await bot.answer_message("Message was unpinned")


@collector.command_with_help(
    "/create-chat",
    description="Create new chat and get its mention",
)
async def create_chat(message: IncomingMessage, bot: Bot) -> None:
    """`/create-chat chat_type chat_name [shared_history]`

    Create new chat and get its mention.

    • `chat_type` - One of: `personal_chat`, `group_chat`, `channel`.
    • `chat_name` - Name for new chat.
    • `shared_history` - Enable shared history for new chat.

    Examples:

    ```bash
    # Create group chat with `@@Your user` named "Test1 chat"
    /create-chat group_chat Test1 chat @@Your user

    # Create group chat with `@@Your user` named "Test1 chat" (shared history enabled)
    /create-chat group_chat Test2 chat shared_history @@Your user
    ```
    """

    if not (match := CREATE_CHAT_ARGS_REGEXP.search(message.argument)):
        await bot.answer_message("**Error:** Missing required arguments")
        return

    chat_type = ChatTypes(match.group("chat_type").upper())
    chat_name = match.group("chat_name")
    shared_history = bool(match.group("shared_history"))

    user_mentions = user_mentions_without_bot(message)
    if chat_type == ChatTypes.PERSONAL_CHAT and len(user_mentions) != 1:
        await bot.answer_message(
            "**Error:** Only one mention required and allowed for personal chat"
        )
        return

    if not user_mentions:
        await bot.answer_message("**Error:** At least one user mention required")
        return

    try:
        chat_id = await bot.create_chat(
            bot_id=message.bot.id,
            name=chat_name,
            chat_type=chat_type,
            huids=[user.entity_id for user in user_mentions],  # type: ignore
            shared_history=shared_history,
        )
    except (ChatCreationProhibitedError, ChatCreationError) as exc:
        await bot.answer_message(str(exc))
        return

    text = "Channel created" if chat_type == ChatTypes.CHANNEL else "Chat created"
    await bot.answer_message(
        f"{text}: {Mention.chat(chat_id, chat_name)}"
    )  # noqa: WPS221

    if chat_type == ChatTypes.PERSONAL_CHAT:
        await bot.answer_message(text)
