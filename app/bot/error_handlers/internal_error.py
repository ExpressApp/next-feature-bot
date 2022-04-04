"""Handler to work with unexpected errors."""

from pybotx import Bot, BotShuttingDownError, IncomingMessage

from app.logger import logger


async def internal_error_handler(
    message: IncomingMessage, bot: Bot, exc: Exception
) -> None:
    logger.exception("Internal error:")

    await bot.answer_message(
        "**Error:** internal error, please contact your system administrator",
        # We can't receive callback when bot is shutting down
        wait_callback=isinstance(exc, BotShuttingDownError),
    )
