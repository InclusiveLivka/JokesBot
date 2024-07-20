import logging

from aiogram import F, Router
from aiogram.types import Message

from app.database.engine import read_jokes_from_sqlite

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == 'Лидеры')
async def get_leaderboard(message: Message) -> None:
    """
    Handles the 'Лидеры' command.

    Args:
        message (Message): Incoming message from the user.
    """
    try:
        leaderboard = await read_jokes_from_sqlite()
        if leaderboard:
            leaderboard_sorted = sorted(
                leaderboard, key=lambda x: x[3], reverse=True
            )

            # выбор трёх анекдотов с высшим баллом
            top_three_jokes = leaderboard_sorted[:3]
            leaderboard_text = "\n".join(
                [f"{joke[0]} (Оценка: {joke[3]})" for joke in top_three_jokes])

            await message.answer(
                "Топ 3 анекдота с высшим баллом:\n" + leaderboard_text
            )
            logger.info(f"Sent leaderboard to user {message.from_user.id}")
        else:

            await message.answer("Нет анекдотов с двумя оценками.")
            logger.info(
                f"No jokes with two grades for user {message.from_user.id}")
    except Exception as e:
        await message.answer("Произошла ошибка при получении лидеров.")
        logger.error(f"Error while getting leaderboard: {e}")
