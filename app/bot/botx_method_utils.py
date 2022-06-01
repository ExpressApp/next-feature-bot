import json
from typing import Any, Dict, Optional, Union, cast
from uuid import UUID

from aiofiles.tempfile import NamedTemporaryFile
from pybotx import Bot, File
from pybotx.missing import Missing, Undefined
from pybotx.models.attachments import IncomingFileAttachment, OutgoingAttachment

BOTX_RESPONSE_LABEL_TEMPLATE = "**Status code:** `{status_code}`\n**Response payload:**"


async def send_json_snippet(
    bot: Bot,
    label: str,
    snippet: str,
    filename: str,
    recipient: Optional[UUID] = None,
    bot_id: Optional[UUID] = None,
) -> None:
    async def send_message(  # noqa: WPS430
        text: str, attachment: Missing[OutgoingAttachment] = Undefined
    ) -> None:
        if recipient and bot_id:
            await bot.send_message(
                bot_id=bot_id, chat_id=recipient, body=text, file=attachment
            )
            return

        await bot.answer_message(text, file=attachment)

    maximum_text_length = 4096
    text = label + f"\n```json\n{snippet}\n```"

    if len(text) <= maximum_text_length:
        await send_message(text)
        return

    async with NamedTemporaryFile("wb+") as async_buffer:
        await async_buffer.write(snippet.encode())
        await async_buffer.seek(0)

        payload_file = await OutgoingAttachment.from_async_buffer(
            async_buffer, filename
        )

    await send_message(label, payload_file)


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
