"""Handlers for testing search."""

from uuid import UUID

from pybotx import Bot, IncomingMessage, MentionBuilder, UserNotFoundError

from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.regular_expressions import SEARCH_USER_REGEXP

collector = HandlerCollectorWithHelp()


@collector.command_with_help(
    "/search-user", description="Seach user by huid, email or ad"
)
async def search_user(message: IncomingMessage, bot: Bot) -> None:  # noqa: WPS231
    """`/search-user attr_name attr_value`

    Seach user by huid, email or ad.

    • `attr_name` - User attribute to search by: (`huid`, `ad`, `email`).
    • `attr_value` - Attribute value.

    Examples:

    ```bash
    # Search user by huid `123e4567-e89b-12d3-a456-426655440000`
    /search-user huid 123e4567-e89b-12d3-a456-426655440000

    # Search user by ad `ad_login ad_domain`
    /search-user ad ad_login ad_domain

    # Search user by email `foo@bar.baz`
    /search-user email foo@bar.baz
    ```
    """

    if not (match := SEARCH_USER_REGEXP.search(message.argument)):
        await bot.answer_message("**Error:** Invalid arguments")
        return

    if match.group("by_huid"):
        try:
            user = await bot.search_user_by_huid(
                bot_id=message.bot.id, huid=UUID(match.group("huid"))
            )
        except ValueError:
            await bot.answer_message("**Error:** Invalid huid")
            return

        except UserNotFoundError:
            await bot.answer_message("**Error:** User not found")
            return

    elif match.group("by_ad"):
        try:
            user = await bot.search_user_by_ad(
                bot_id=message.bot.id,
                ad_login=match.group("ad_login"),
                ad_domain=match.group("ad_domain"),
            )
        except UserNotFoundError:
            await bot.answer_message("**Error:** User not found")
            return

    elif match.group("by_email"):
        try:
            user = await bot.search_user_by_email(
                bot_id=message.bot.id, email=match.group("email")
            )
        except UserNotFoundError:
            await bot.answer_message("**Error:** User not found")
            return

    else:
        raise RuntimeError(f"Unknown search attr {message.argument}")

    await bot.answer_message(f"User found: {MentionBuilder.contact(user.huid)}")
