from aiogram import Dispatcher

from .start import router as start_router
from .joke import router as joke_router
from .grade import router as grade_router
from .leaderboard import router as leaderboard_router


def setup_routers(dp: Dispatcher) -> None:
    """
    Set up routers for the dispatcher.

    Args:
        dp (Dispatcher): The dispatcher instance.
    """
    dp.include_router(start_router)
    dp.include_router(joke_router)
    dp.include_router(grade_router)
    dp.include_router(leaderboard_router)
