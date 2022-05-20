import json

from pybotx import Bot, ChatTypes, IncomingMessage, InternalBotNotificationEvent
from pybotx.missing import Undefined

from app.bot.botx_method_utils import send_json_snippet
from app.bot.handler_with_help import HandlerCollectorWithHelp

collector = HandlerCollectorWithHelp()


@collector.internal_bot_notification
async def internal_bot_notification_handler(
    event: InternalBotNotificationEvent, bot: Bot
) -> None:
    await send_json_snippet(
        bot,
        "Received internal bot notification:",
        json.dumps(event.data, ensure_ascii=False, indent=2),
        "notification.json",
    )


@collector.command_with_help(
    "/internal-bot-notification",
    description="Send internal bot notification to another bot in chat.",
)
async def send_internal_bot_notification(message: IncomingMessage, bot: Bot) -> None:
    """send internal bot notification to another bot in chat.

    Arguments:
        `<text>` *(optional: [default: ping])* - text to send.
        `<@@mention>` *(optional: [default: all chat members])* - recipients."""

    if message.chat.type != ChatTypes.GROUP_CHAT:
        await bot.answer_message(
            "Command may be used in group chat only.",
        )
        return

    recipients = [
        mention.entity_id for mention in message.mentions.contacts
    ] or Undefined
    text = message.argument or "ping"

    sync_id = await bot.send_internal_bot_notification(
        bot_id=message.bot.id,
        chat_id=message.chat.id,
        data={"message": text},
        recipients=recipients,
    )

    await bot.answer_message(
        f"Internal bot notification sent. Sync id `{sync_id}`",
    )
