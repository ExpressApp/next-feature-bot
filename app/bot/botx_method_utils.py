import json
from typing import Any, Dict, Optional, Union, cast

import aiofiles
from aiofiles.tempfile import NamedTemporaryFile
from aiofiles.threadpool import AsyncBufferedReader
from pybotx import Bot, File
from pybotx.models.attachments import IncomingFileAttachment, OutgoingAttachment

from app.settings import settings

BOTX_RESPONSE_LABEL_TEMPLATE = "**Status code:** `{status_code}`\n**Response payload:**"


async def send_json_snippet(bot: Bot, label: str, snippet: str, filename: str) -> None:
    maximum_text_length = 4096
    text = label + f"\n```json\n{snippet}\n```"

    if len(text) <= maximum_text_length:
        await bot.answer_message(text)
        return

    async with NamedTemporaryFile("wb+") as async_buffer:
        await async_buffer.write(snippet.encode())
        await async_buffer.seek(0)

        payload_file = await OutgoingAttachment.from_async_buffer(
            async_buffer, filename
        )

    await bot.answer_message(label, file=payload_file)


async def get_request_payload(
    raw_embedded_payload: str, attachment: Optional[Union[File, IncomingFileAttachment]]
) -> Optional[Dict[str, Any]]:
    if raw_embedded_payload and attachment:
        raise ValueError(
            "**Error:** You can't specify payload "
            "in both message body and message attachment at the same time"
        )

    if attachment:
        async with attachment.open() as fo:
            attachment_content = await fo.read()

        try:
            attachment_payload = json.loads(attachment_content)
        except (json.JSONDecodeError, UnicodeDecodeError) as attachment_decoding_exc:
            raise ValueError(f"**Error:**\n{attachment_decoding_exc}")

        return cast(Dict[str, Any], attachment_payload)

    if not raw_embedded_payload:
        return None

    try:
        embedded_payload = json.loads(raw_embedded_payload)
    except (json.JSONDecodeError, UnicodeDecodeError) as embedded_decoding_exc:
        raise ValueError(f"**Error:**\n{embedded_decoding_exc}")

    return cast(Dict[str, Any], embedded_payload)


async def get_files() -> Dict[str, bytes]:
    read_files = {}
    for file in settings.FILES_DIR.iterdir():
        async with aiofiles.open(file, "rb") as f:
            suffix = "".join(file.suffixes)[1:]
            read_files[suffix] = await f.read()
    return read_files
