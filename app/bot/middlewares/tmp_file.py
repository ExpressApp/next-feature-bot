"""Middleware to make temporary file for writing users list on CTS."""

from aiofiles.tempfile import NamedTemporaryFile, TemporaryDirectory
from pybotx import Bot, IncomingMessage, IncomingMessageHandlerFunc


async def tmp_file_middleware(
    message: IncomingMessage, bot: Bot, call_next: IncomingMessageHandlerFunc
) -> None:
    async with TemporaryDirectory() as tmp_dir:
        async with NamedTemporaryFile(mode="w", delete=False, dir=tmp_dir) as tmp_file:
            bot.state.tmp_file = tmp_file
            await call_next(message, bot)
