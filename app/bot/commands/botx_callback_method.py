"""Handlers calling botx method directly with callback support."""

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional
from uuid import UUID

from pybotx import Bot, IncomingMessage
from pybotx.client.authorized_botx_method import AuthorizedBotXMethod
from pybotx.client.exceptions.callbacks import CallbackNotReceivedError
from pybotx.client.exceptions.http import InvalidBotXResponsePayloadError
from pybotx.models.api_base import VerifiedPayloadBaseModel

from app.bot.botx_method_utils import (
    BOTX_RESPONSE_LABEL_TEMPLATE,
    get_request_payload,
    send_json_snippet,
)
from app.bot.formatting import pformat_str_json
from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.regular_expressions import BOTX_METHOD_ARGS_REGEXP

collector = HandlerCollectorWithHelp()


class BotXAPISyncIdResult(VerifiedPayloadBaseModel):
    sync_id: UUID


class BotXAPIMethodResponsePayload(VerifiedPayloadBaseModel):
    status: Literal["ok"]
    result: BotXAPISyncIdResult  # noqa: WPS110


@dataclass
class CallBotXCallbackMethodResult:
    status_code: int
    raw_payload: str
    sync_id: UUID


class CallBotXMethod(AuthorizedBotXMethod):
    async def execute(
        self, method: str, path_with_query: str, payload_dict: Optional[Dict[str, Any]]
    ) -> CallBotXCallbackMethodResult:
        response = await self._botx_method_call(
            method,
            self._build_url(path_with_query),
            json=payload_dict,
        )

        api_model = self._verify_and_extract_api_model(
            BotXAPIMethodResponsePayload,
            response,
        )

        await self._process_callback(
            api_model.result.sync_id,
            wait_callback=False,
            callback_timeout=None,
        )

        return CallBotXCallbackMethodResult(
            status_code=response.status_code,
            raw_payload=response.text,
            sync_id=api_model.result.sync_id,
        )


@collector.command_with_help(
    "/botx-callback-method", description="Call BotX method directly (callback support)"
)
async def botx_callback_method_handler(  # noqa: WPS210, WPS217
    message: IncomingMessage, bot: Bot
) -> None:
    """`/botx-callback-method method path [message_payload] [attachment_payload]`

    Call BotX method directly. Method should return `sync_id` and send callback to bot.

    • `method` - HTTP-method to call.
    • `path_with_query` - Endpoint path with query.
    • `message_payload` - Method payload (should be surrounded with code block).
    • `attachment_payload` - Method payload. Can't be used with `message_payload`.

    Examples:

    ````bash
    # Call GET endpoint
    /botx-callback-method GET /api/foo

    # Call GET endpoint with query
    /botx-callback-method GET /api/foo?bar=baz

    # Call POST endpoint with message payload
    /botx-callback-method POST /api/foo
    ```
    {"bar": "baz"}
    ```

    # Call POST endpoint with message payload without ```
    /botx-callback-method POST /api/foo
    {"bar": "baz"}

    # Call POST endpoint with query and message payload
    /botx-callback-method POST /api/foo?bar=baz
    ```
    {"quux": "1"}
    ```

    # Call POST endpoint with attachment payload
    /botx-callback-method POST /api/foo
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
        callbacks_manager=bot._callback_manager,  # noqa: WPS437
    )

    try:
        call_result = await botx_method.execute(
            http_method, path_with_query, request_payload
        )
    except InvalidBotXResponsePayloadError:
        await bot.answer_message(
            "sync_id cannot be found in method result.\n"
            "Use `/botx-method` comand instead or "
            "contact your system administrator if method supports callback."
        )
        return
    except Exception as callback_exc:
        await bot.answer_message(f"**Error:**\n{callback_exc}")
        return

    try:
        callback = await bot.wait_botx_method_callback(
            call_result.sync_id,
            timeout=5,
        )
    except CallbackNotReceivedError:
        await bot.answer_message("Callback is not recieved.")
        return

    label = BOTX_RESPONSE_LABEL_TEMPLATE.format(status_code=call_result.status_code)
    response_payload = pformat_str_json(call_result.raw_payload)
    await send_json_snippet(bot, label, response_payload, "payload.json")

    callback_payload = pformat_str_json(callback.json())
    await send_json_snippet(bot, "**Callback:**", callback_payload, "callback.json")
