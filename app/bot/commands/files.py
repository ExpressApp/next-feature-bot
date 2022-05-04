"""Handlers for repeating incoming messages."""

from uuid import UUID

from aiofiles.tempfile import NamedTemporaryFile
from pybotx import (
    Bot,
    ChatNotFoundError,
    FileDeletedError,
    FileMetadataNotFound,
    IncomingMessage,
    OutgoingAttachment,
)

from app.bot.botx_method_utils import get_files
from app.bot.handler_with_help import HandlerCollectorWithHelp

collector = HandlerCollectorWithHelp()


@collector.command_with_help(
    "/echo-file", description="Send received attachment back to user"
)
async def echo_file_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/echo-file attachment`

    Sends received attachment back to user.

    • `attachment` - Message attachment.

    Examples:

    ```bash
    /echo-file
    <attachment>
    ```
    """
    if not (attached_file := message.file):
        await bot.answer_message("**Error:** Attached file is required")
        return

    if attached_file.is_async_file:
        await bot.answer_message("**Error:** Async-files are not supported")
        return

    await bot.answer_message("", file=attached_file)


@collector.command_with_help("/upload-file", description="Upload file to fileservice")
async def upload_file(message: IncomingMessage, bot: Bot) -> None:
    """`/upload-file attachment`

    Upload file to fileservice and print its id.

    • `attachment` - Message attachment.

    ```bash
    /upload-file
    <attachment>
    ```
    """

    if not message.file:
        await bot.answer_message("**Error:** Attached file is required")
        return

    async with message.file.open() as async_buffer:
        try:
            uploaded_file = await bot.upload_file(
                bot_id=message.bot.id,
                chat_id=message.chat.id,
                filename=message.file.filename,
                async_buffer=async_buffer,
            )
        except ChatNotFoundError as error:
            await bot.answer_message(str(error))
            return

        await bot.answer_message(f"File_id: `{uploaded_file._file_id}`")  # noqa:WPS437


@collector.command_with_help(
    "/download-file",
    description="Download file",
)
async def download_file(message: IncomingMessage, bot: Bot) -> None:
    """`/download-file attachment_id`

    Download file from fileservice by its id.

    • `attachment_id` - Attachment id on fileservice (from `/upload-file` command).

    ```bash
    # Download file with id 123e4567-e89b-12d3-a456-426655440000
    /download-file 123e4567-e89b-12d3-a456-426655440000
    ```
    """

    if len(message.arguments) != 2:
        await bot.answer_message("**Error:** Invalid arguments")
        return

    file_id_str, filename = message.arguments

    try:
        file_id = UUID(file_id_str)
    except ValueError:
        await bot.answer_message("**Error:** File id is invalid")
        return

    async with NamedTemporaryFile("wb+") as async_buffer:
        try:
            await bot.download_file(
                bot_id=message.bot.id,
                chat_id=message.chat.id,
                file_id=file_id,
                async_buffer=async_buffer,
            )
        except (FileMetadataNotFound, ChatNotFoundError, FileDeletedError) as error:
            await bot.answer_message(str(error))
            return

        outgoing_file = await OutgoingAttachment.from_async_buffer(
            async_buffer=async_buffer, filename=filename
        )

        await bot.answer_message("File", file=outgoing_file)


@collector.command_with_help(
    "/send-file",
    description="Send file by extension",
)
async def send_file(message: IncomingMessage, bot: Bot) -> None:
    """`/send-file extension`

    Send sample file with required extension.

    • `extension` - Extension of target file.

    ```bash
    # Send pdf file
    /send-file pdf
    ```
    """

    extension = message.argument
    files = await get_files()

    if not extension:
        text = (
            "Argument required: `/send-file <file_ext>`\n"
            f"Extensions: {set(files.keys())}"
        )
        await bot.answer_message(text)
        return

    try:
        file_sample = OutgoingAttachment(files[extension], f"file.{extension}")
    except KeyError:
        await bot.answer_message(f"Unknown extension: {extension}")
        return

    await bot.send_message(
        bot_id=message.bot.id,
        chat_id=message.chat.id,
        body="",
        file=file_sample,
    )
