"""Handlers calling botx method directly."""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from pybotx import Bot, IncomingMessage
from pybotx.client.authorized_botx_method import AuthorizedBotXMethod

from app.bot.botx_method_utils import (
    BOTX_RESPONSE_LABEL_TEMPLATE,
    get_request_payload,
    send_json_snippet,
)
from app.bot.formatting import pformat_str_json
from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.regular_expressions import BOTX_METHOD_ARGS_REGEXP

collector = HandlerCollectorWithHelp()


@dataclass
class CallBotXMethodResult:
    status_code: int
    payload: str


class CallBotXMethod(AuthorizedBotXMethod):
    async def execute(
        self, method: str, path_with_query: str, payload_dict: Optional[Dict[str, Any]]
    ) -> CallBotXMethodResult:
        response = await self._botx_method_call(
            method,
            self._build_url(path_with_query),
            json=payload_dict,
        )

        return CallBotXMethodResult(
            status_code=response.status_code, payload=response.text
        )


@collector.command_with_help("/botx-method", description="Call BotX method directly")
async def botx_method_handler(  # noqa: WPS210, WPS217
    message: IncomingMessage, bot: Bot
) -> None:
    """`/botx-method method path [message_payload] [attachment_payload]`

    Call BotX method directly.

    • `method` - HTTP-method to call.
    • `path_with_query` - Endpoint path with query.
    • `message_payload` - Method payload (should be surrounded with code block).
    • `attachment_payload` - Method payload. Can't be used with `message_payload`.

    Examples:

    ````bash
    # Call GET endpoint
    /botx-method GET /api/foo

    # Call GET endpoint with query
    /botx-method GET /api/foo?bar=baz

    # Call POST endpoint with message payload
    /botx-method POST /api/foo
    ```
    {"bar": "baz"}
    ```

    # Call POST endpoint with message payload without ```
    /botx-callback-method POST /api/foo
    {"bar": "baz"}

    # Call POST endpoint with query and message payload
    /botx-method POST /api/foo?bar=baz
    ```
    {"quux": "1"}
    ```

    # Call POST endpoint with attachment payload
    /botx-method POST /api/foo
    <attached_file>
    ````
    """

    if not (match := BOTX_METHOD_ARGS_REGEXP.search(message.argument)):
        await bot.answer_message("Invalid arguments.")
        return

    http_method = match.group("http_method")
    path_with_query = match.group("path_with_query")
    raw_embedded_payload = match.group("embedded_payload")

    try:
        request_payload = await get_request_payload(raw_embedded_payload, message.file)
    except ValueError as payload_exc:
        await bot.answer_message(payload_exc.args[0])
        return

    botx_method = CallBotXMethod(
        sender_bot_id=message.bot.id,
        httpx_client=bot._httpx_client,  # noqa: WPS437 (Hotplugging method)
        bot_accounts_storage=bot._bot_accounts_storage,  # noqa: WPS437
    )

    try:
        call_result = await botx_method.execute(
            http_method, path_with_query, request_payload
        )
    except Exception as exc:
        await bot.answer_message(f"**Error:**\n{exc}")
        return

    label = BOTX_RESPONSE_LABEL_TEMPLATE.format(status_code=call_result.status_code)
    response_payload = pformat_str_json(call_result.payload)
    await send_json_snippet(
        message.bot.id, message.chat.id, bot, label, response_payload, "payload.json"
    )
