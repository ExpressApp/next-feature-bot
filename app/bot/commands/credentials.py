from uuid import UUID

from pybotx import Bot, BotAccountWithSecret, IncomingMessage

from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.regular_expressions import ADD_BOT_CREDENIALS_REGEXP

collector = HandlerCollectorWithHelp()


@collector.command_with_help("/add-credentials", description="Add new bot credentials")
async def add_credentials_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/add-credentials host secret_key bot_id`

    Add new bot credentials.

    • `host` - Bot host (same as admin-site host).
    • `secret` - Secret key from bot profile.
    • `bot_id` - ID from bot profile.

    Examples:

    ```bash
    # Add bot credentials
    /add-credentials cts.example.com 70261ca27012d06ff660b3f5d2b05782 123e4567-e89b-12d3-a456-426614174000
    ```
    """
    if not (match := ADD_BOT_CREDENIALS_REGEXP.search(message.argument)):
        await bot.answer_message("**Error:** Missing required arguments")
        return

    host = match.group("host")
    secret_key = match.group("secret_key")

    try:
        bot_id = UUID(match.group("bot_id"))
    except ValueError:
        await bot.answer_message("**Error:** Invalid bot id")
        return

    # Normally bot accounts doesn't added on the fly
    bot._bot_accounts_storage._bot_accounts.append(  # noqa: WPS437
        BotAccountWithSecret(id=bot_id, host=host, secret_key=secret_key)
    )

    await bot.answer_message("Credentials was added")
