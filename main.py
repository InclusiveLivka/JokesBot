import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError

from app.handlers import setup_routers
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start_bot() -> None:
    """
    Initialize and start the bot with polling.

    This function sets up the bot instance, dispatcher, and includes necessary
    routers.
    It starts the polling process to receive updates from Telegram.
    """
    logger.info("Starting bot...")

    # Создание экземпляра бота
    bot = Bot(token=BOT_TOKEN)
    logger.info("Bot instance created.")

    # Создание диспетчера
    dp = Dispatcher()
    logger.info("Dispatcher instance created.")

    # Включение роутеров
    setup_routers(dp)
    logger.info("Routers included.")

    # Запуск поллинга
    try:

        await dp.start_polling(bot)
    except TelegramAPIError as e:
        logger.error(f"Telegram API Error: {e}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    finally:
        # Закрытие бота
        await bot.session.close()
        logger.info("Bot session closed.")


async def main() -> None:
    """
    Main entry point for the bot application.

    This function runs the start_bot coroutine using asyncio.
    """
    await start_bot()

if __name__ == "__main__":
    logger.info("Starting main application...")
    asyncio.run(main())
    logger.info("Main application stopped.")
