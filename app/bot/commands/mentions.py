"""Handlers for testing mentions."""

from typing import List

from pybotx import Bot, IncomingMessage, Mention

from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.mentions import user_mentions_without_bot

collector = HandlerCollectorWithHelp()


def join_mentions(mentions_group: List[Mention]) -> str:
    return ", ".join(str(mention) for mention in mentions_group)


@collector.command_with_help(
    "/print-mentions", description="Print received mentions grouped by theirs types"
)
async def print_mentions_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/print-mentions [mentions_of_any_type...]

    Print received mentions grouped by theirs types.

    • `mentions_of_any_type...` - Mentions of any type: `@all`, `@user`,
      `@@user_contact`, `##group_chat`, `##channel`. Could be specified in any position.

    Examples:

    ```bash
    # Print `@all` mention
    /print-mentions @all

    # Print user's mention and contact
    /print-mentions @user1 @@user1
    ```
    """

    if not (mentions := message.mentions):
        await bot.answer_message("**Error:** Mentions are required")
        return

    answer_body = "\n".join(
        [
            "**You've send these mentions to bot**",
            f"Sender's mention: {Mention.user(message.sender.huid)}",
            f"Users: {join_mentions(mentions.users)}",
            f"Contacts: {join_mentions(mentions.contacts)}",
            f"Chats: {join_mentions(mentions.chats)}",
            f"Channels: {join_mentions(mentions.channels)}",
            f"All users are mentioned: {mentions.all_users_mentioned}",
        ]
    )

    await bot.answer_message(answer_body)


@collector.command_with_help(
    "/get-huids",
    description="Get huids list from passed contact mentions",
)
async def huids_by_mentions(message: IncomingMessage, bot: Bot) -> None:
    """`/get-huids @@user...`

    Get huids list from passed contact mentions.

    • `@@user...` - User contact mentions (via `@@`). Could be specified in any position.

    Examples:

    ```bash
    # Get huids for `@@User 1` and `@@User 2`
    /get-huids @@User 1 @@User 2
    ```
    """

    user_mentions = user_mentions_without_bot(message)
    if not user_mentions:
        await bot.answer_message("**Error:** No user mentions specified")
        return

    sorted_user_mentions = sorted(
        user_mentions, key=lambda mention: mention.name  # type: ignore
    )

    text = "\n".join(
        f"{mention.name}: `{mention.entity_id}`" for mention in sorted_user_mentions
    )

    await bot.answer_message(text)
