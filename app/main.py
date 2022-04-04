"""Application with configuration for events, routers and middleware."""
from fastapi import FastAPI

from app.api.routers import router
from app.bot.bot import bot
from app.bot.datastructures import CTSEventsListeners


async def startup() -> None:
    await bot.startup()
    bot.state.chats_listening_cts_events = CTSEventsListeners()


def get_application() -> FastAPI:
    """Create configured server application instance."""
    application = FastAPI(title="next-feature-bot")
    application.state.bot = bot

    application.add_event_handler("startup", startup)
    application.add_event_handler("shutdown", bot.shutdown)

    application.include_router(router)

    return application


app = get_application()
