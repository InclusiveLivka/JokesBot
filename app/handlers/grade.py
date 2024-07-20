import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.database.engine import write_grade
from app.utils.get_jokes import get_random_joke
from app.keyboards import inline

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data)
async def get_grade(callback: CallbackQuery) -> None:
    """
    Handles user grade input.

    Args:
        callback (CallbackQuery): Incoming callback query from the user.
    """
    try:
        grade: int = int(callback.data)
        await callback.answer("Сохранено")
        joke: str = callback.message.text
        await write_grade(joke, grade)
        logger.info(
            f"Saved grade {grade} for joke from user {callback.from_user.id}")

        # Удаляем кнопки
        await callback.message.edit_reply_markup(reply_markup=None)

        # Отправляем новый анекдот
        new_joke: str = get_random_joke()
        await callback.message.answer(
            new_joke, reply_markup=inline.score_keyboard
        )
    except ValueError as e:
        await callback.answer("Некорректная оценка.")
        logger.error(f"Invalid grade value: {e}")
