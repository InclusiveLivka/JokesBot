import logging

from aiogram import F, Router
from aiogram.types import Message
from aiogram.dispatcher.router import Router

from app.keyboards import replay

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == '/start')
async def start(message: Message) -> None:
    """
    Handles the /start command.

    Args:
        message (Message): Incoming message from the user.
    """
    logger.info(f"Received /start command from {message.from_user.id}")
    await message.answer(
        "Привет, я могу рассказать анекдот, а ты его оценишь!",
        reply_markup=replay.menu
    )
    logger.info("Sent start message to the user")
