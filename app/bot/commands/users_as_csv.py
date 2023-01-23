"""Handler for getting users list on CTS."""

from enum import Enum

import aiofiles
from aiocsv.writers import AsyncDictWriter
from pybotx import Bot, IncomingMessage, OutgoingAttachment

from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.middlewares.tmp_file import tmp_file_middleware
from app.bot.regular_expressions import USERS_AS_CSV_REGEXP

collector = HandlerCollectorWithHelp()


class StrEnum(str, Enum):  # noqa: WPS600
    """Base enum."""


class CSVFieldNames(StrEnum):
    huid = "HUID"
    ad_login = "AD Login"
    domain = "Domain"
    ad_email = "AD E-mail"
    username = "Name"
    sync_source = "Sync source"
    active = "Active"
    kind = "Kind"
    department = "Department"
    position = "Position"


@collector.command_with_help(
    "/users-as-csv",
    description="Get CTS users as CSV",
    middlewares=[tmp_file_middleware],
)
async def users_as_csv_handler(  # noqa: WPS210
    message: IncomingMessage, bot: Bot
) -> None:
    """`/users-as-csv cts_user unregistered botx`

    Get users list on the current CTS in CSV format.

    • `cts_user` - Include users with `cts_user` type.
    • `unregistered` - Include users with `unregistered` type.
    • `botx` - Include users with `botx` type.

    ```bash
    /users-as-csv true true false
    ```
    """

    if not (match := USERS_AS_CSV_REGEXP.search(message.argument)):
        await bot.answer_message("Invalid arguments.")
        return

    cts_user = match.group("cts_user") or True
    if isinstance(cts_user, str):
        cts_user = convert_arg_to_bool(cts_user)

    unregistered = match.group("unregistered") or True
    if isinstance(unregistered, str):
        unregistered = convert_arg_to_bool(unregistered)

    botx = match.group("botx") or False
    if isinstance(botx, str):
        botx = convert_arg_to_bool(botx)

    async with bot.users_as_csv(
        bot_id=message.bot.id, cts_user=cts_user, unregistered=unregistered, botx=botx
    ) as users:
        writer = AsyncDictWriter(
            bot.state.tmp_file,
            fieldnames=[field.value for field in CSVFieldNames],
        )
        await writer.writeheader()

        async for user in users:
            if isinstance(user.sync_source, str):
                sync_source = user.sync_source
            else:
                sync_source = user.sync_source.value

            await writer.writerow(
                {
                    CSVFieldNames.huid: user.huid,
                    CSVFieldNames.ad_login: user.ad_login,
                    CSVFieldNames.domain: user.ad_domain,
                    CSVFieldNames.ad_email: user.email,
                    CSVFieldNames.username: user.username,
                    CSVFieldNames.sync_source: sync_source,
                    CSVFieldNames.active: user.active,
                    CSVFieldNames.kind: user.user_kind.value,
                    CSVFieldNames.department: user.department,
                    CSVFieldNames.position: user.position,
                }
            )

        filename = bot.state.tmp_file.name

    async with aiofiles.open(filename, "rb") as async_buffer:
        attachment = await OutgoingAttachment.from_async_buffer(
            async_buffer=async_buffer,
            filename="users_as_csv.csv",
        )

    await bot.send_message(
        bot_id=message.bot.id,
        chat_id=message.chat.id,
        body="",
        file=attachment,
    )


def convert_arg_to_bool(arg: str) -> bool:
    return arg.strip() == "true"
