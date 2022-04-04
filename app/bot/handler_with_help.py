"""Wrapper on HandlerCollector to pride additional commands."""

from inspect import cleandoc
from typing import Callable, Dict, Optional, Sequence, Union

from pybotx import HandlerCollector
from pybotx.bot.handler import IncomingMessageHandlerFunc, Middleware, VisibleFunc


class HandlerCollectorWithHelp(HandlerCollector):
    def __init__(self, middlewares: Optional[Sequence[Middleware]] = None) -> None:
        super().__init__(middlewares)
        self._helps_for_commands: Dict[str, str] = {}

    def command_with_help(
        self,
        command_name: str,
        visible: Union[bool, VisibleFunc] = True,
        description: Optional[str] = None,
        middlewares: Optional[Sequence[Middleware]] = None,
    ) -> Callable[[IncomingMessageHandlerFunc], IncomingMessageHandlerFunc]:
        """Decorate command handler."""

        def decorator(
            handler_func: IncomingMessageHandlerFunc,
        ) -> IncomingMessageHandlerFunc:
            assert handler_func.__doc__, "docstring required to use command_with_help()"

            self._helps_for_commands[command_name] = cleandoc(handler_func.__doc__)

            handler_collector_decorator = self.command(
                command_name=command_name,
                visible=visible,
                description=description,
                middlewares=middlewares,
            )

            return handler_collector_decorator(handler_func)

        return decorator

    async def get_help_message(
        self,
        command_name: str,
    ) -> str:
        return self._helps_for_commands[command_name]

    def _include_collector(self, other: "HandlerCollector") -> None:
        super()._include_collector(other)

        if isinstance(other, HandlerCollectorWithHelp):
            self._helps_for_commands.update(other._helps_for_commands)  # noqa: WPS437
