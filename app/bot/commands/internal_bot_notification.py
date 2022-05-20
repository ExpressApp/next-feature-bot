from pybotx import Bot, InternalBotNotificationEvent

from app.bot.botx_method_utils import send_json_snippet
from app.bot.formatting import pformat_json
from app.bot.handler_with_help import HandlerCollectorWithHelp

collector = HandlerCollectorWithHelp()


@collector.internal_bot_notification
async def internal_bot_notification_handler(
    event: InternalBotNotificationEvent, bot: Bot
) -> None:
    await send_json_snippet(
        bot,
        "Received internal bot notification:",
        pformat_json(event.data),
        "notification.json",
    )
