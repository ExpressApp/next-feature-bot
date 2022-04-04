"""Handlers for markup experiments."""

from typing import Type, Union, cast

from pybotx import Bot, BubbleMarkup, Button, IncomingMessage, KeyboardMarkup

from app.bot.handler_with_help import HandlerCollectorWithHelp
from app.bot.regular_expressions import CREATE_MARKUP_ARGS_REGEXP

collector = HandlerCollectorWithHelp()

Markup = Union[BubbleMarkup, KeyboardMarkup]


def _create_markup(
    rows: int,
    columns: int,
    markup_cls: Type[Markup],
) -> Markup:
    bubbles = markup_cls()

    for index in range(rows * columns):
        bubbles.add_button("", str(index), new_row=(index % columns == 0))

    return bubbles


@collector.command_with_help("/bubble", description="Create matrix of bubbles buttons")
async def bubble_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/bubble rows columns [buttons_auto_adjust]`

    Create matrix of bubbles buttons.

    • `rows` - Number of rows in matrix.
    • `columns` - Number of columns in matrix.
    • `buttons_auto_adjust` - Move buttons to next line if there isn't
      enough space for labels.
    """
    if not (match := CREATE_MARKUP_ARGS_REGEXP.search(message.argument)):
        await bot.answer_message("Invalid arguments.")
        return

    rows = int(match.group("rows"))
    columns = int(match.group("columns"))
    markup_auto_adjust = bool(match.group("buttons_auto_adjust"))

    bubbles = cast(BubbleMarkup, _create_markup(rows, columns, BubbleMarkup))
    await bot.answer_message(
        message.body, bubbles=bubbles, markup_auto_adjust=markup_auto_adjust
    )


@collector.command_with_help(
    "/keyboard", description="Create matrix of keyboard buttons"
)
async def keyboard_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/keyboard rows columns [buttons_auto_adjust]`

    Create matrix of keyboard buttons.

    • `rows` - Number of rows in matrix.
    • `columns` - Number of columns in matrix.
    • `buttons_auto_adjust` - Move buttons to next line if there isn't
      enough space for labels.
    """

    if not (match := CREATE_MARKUP_ARGS_REGEXP.search(message.argument)):
        await bot.answer_message("Invalid arguments.")
        return

    rows = int(match.group("rows"))
    columns = int(match.group("columns"))
    markup_auto_adjust = bool(match.group("buttons_auto_adjust"))

    keyboard = cast(KeyboardMarkup, _create_markup(rows, columns, KeyboardMarkup))
    await bot.answer_message(
        message.body, keyboard=keyboard, markup_auto_adjust=markup_auto_adjust
    )


def build_sized_markup(markup_cls: Type[Markup]) -> Markup:
    sizes = [
        [1, 2, 1],
        [1, 2, 3, 2, 1],
        [1, 3, 5, 3, 1],
        [1, 3],
        [3, 1],
        [1, 999],
        [999, 1],
        [1, 999, 1],
        [1, 999, 5],
    ]

    return markup_cls(
        [
            [Button(command="", label=str(size), width_ratio=size) for size in row]
            for row in sizes
        ]
    )


@collector.command_with_help(
    "/h-size", description="Create matrixes with buttons of different sizes"
)
async def h_size_handler(message: IncomingMessage, bot: Bot) -> None:
    """`/h-size`

    Create matrixes with buttons of different sizes.

    This command doesn't accept arguments.
    """

    bubbles = cast(BubbleMarkup, build_sized_markup(BubbleMarkup))
    keyboard = cast(KeyboardMarkup, build_sized_markup(KeyboardMarkup))

    await bot.answer_message(message.body, bubbles=bubbles, keyboard=keyboard)
