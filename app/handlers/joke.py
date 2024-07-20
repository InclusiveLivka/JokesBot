import logging

from aiogram import F, Router
from aiogram.types import Message

from app.keyboards import inline
from app.utils.jokes import get_random_joke

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == 'Анекдот')
async def get_joke_handler(message: Message) -> None:
    """
    Handles the 'Анекдот' command.

    Args:
        message (Message): Incoming message from the user.
    """
    try:
        joke: str = get_random_joke()
        await message.answer(joke, reply_markup=inline.score_keyboard)
        logger.info(f"Sent joke to user {message.from_user.id}")
    except TypeError as e:
        await message.answer("Произошла ошибка при получении анекдота.")
        logger.error(f"Error while getting joke: {e}")
