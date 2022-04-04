from pybotx import Bot, BubbleMarkup, IncomingMessage

from app.bot.handler_with_help import HandlerCollectorWithHelp

collector = HandlerCollectorWithHelp()


@collector.command_with_help(
    "/edit-message",
    description="Send widget with counter and control buttons",
)
async def enable_stealth(message: IncomingMessage, bot: Bot) -> None:
    """`/edit-message`

    Send widget with counter and control buttons.

    This command doesn't accept arguments.
    """

    edit_message_template = "Counter: {counter}"

    bubbles = BubbleMarkup()
    bubbles.add_button(
        command="/edit-message",
        label="-",
        data={"operation": "sub"},
    )
    bubbles.add_button(
        command="/edit-message",
        label="+",
        data={"operation": "add"},
        new_row=False,
    )

    if message.source_sync_id:
        counter = message.metadata["counter"]
        operation = message.data["operation"]

        if operation == "add":
            updated_counter = counter + 1
        elif operation == "sub":
            updated_counter = counter - 1
        else:
            raise RuntimeError("Invalid operation")

        text = edit_message_template.format(counter=updated_counter)
        await bot.edit_message(
            bot_id=message.bot.id,
            sync_id=message.source_sync_id,
            body=text,
            metadata={"counter": updated_counter},
        )

    else:
        text = edit_message_template.format(counter=0)
        await bot.answer_message(text, metadata={"counter": 0}, bubbles=bubbles)
