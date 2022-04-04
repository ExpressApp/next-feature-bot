"""Bot subclass allowing to get command help."""

from typing import List, Optional, Sequence

from pybotx import Bot
from pybotx.bot.handler import Middleware
from pybotx.bot.middlewares.exception_middleware import ExceptionHandlersDict

from app.bot.handler_with_help import HandlerCollectorWithHelp


class BotWithHelp(Bot):
    def get_command_help(self, command: str) -> str:
        self._handler_collector: HandlerCollectorWithHelp
        try:
            return self._handler_collector._helps_for_commands[command]  # noqa: WPS437
        except KeyError as exc:
            raise RuntimeError(
                f"Don't you forget to add help for command `{command}`?"
            ) from exc

    @staticmethod
    def _build_main_collector(  # type: ignore # noqa:WPS602
        collectors: Sequence[HandlerCollectorWithHelp],
        middlewares: List[Middleware],
        exception_handlers: Optional[ExceptionHandlersDict] = None,
    ) -> HandlerCollectorWithHelp:
        main_collector = HandlerCollectorWithHelp(middlewares=middlewares)
        main_collector.insert_exception_middleware(exception_handlers)
        main_collector.include(*collectors)

        return main_collector
