"""Handlers for default bot commands and system events."""

import json
from os import environ

from pybotx import Bot, IncomingMessage, StatusRecipient

from app.bot.bot_with_help import BotWithHelp
from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.resources import strings

collector = HandlerCollectorWithHelp()


@collector.default_message_handler
async def default_handler(_: IncomingMessage, bot: Bot) -> None:
    await bot.answer_message("Use `/help` to get available commands.")


@collector.command_with_help(
    "/echo",
    description="Send back the received message body",
)
async def echo_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/echo text`

    Reply incoming text after command.

    • `text` - text that should be replied back.
    """
    await bot.answer_message(message.argument)


@collector.command_with_help("/sender-info", description="Print info about sender")
async def user_info(message: IncomingMessage, bot: Bot) -> None:
    """`/sender-info`

    Print info about sender which is accessible to bot.

    This command doesn't accept arguments.
    """

    assert message.raw_command
    text = "```{0}```".format(
        json.dumps(message.raw_command["from"], sort_keys=True, indent=4)
    )

    await bot.answer_message(text)


@collector.command("/help", description="Get available commands")  # type: ignore
async def help_handler(message: IncomingMessage, bot: BotWithHelp) -> None:

    status_recipient = StatusRecipient.from_incoming_message(message)
    status = await bot.get_status(status_recipient)

    if command_name := message.argument:
        if command_name in status:
            answer_body = bot.get_command_help(command_name)
        else:
            answer_body = f"**Error:** Command `{command_name}` doesn't exist"
    else:
        answer_body = strings.HELP_COMMAND_MESSAGE_TEMPLATE.format(bot_status=status)

    await bot.answer_message(answer_body)


@collector.command("/_debug:git-commit-sha", visible=False)
async def git_commit_sha(_: IncomingMessage, bot: Bot) -> None:
    commit_sha = environ.get("GIT_COMMIT_SHA") or "<undefined>"
    await bot.answer_message(commit_sha)
