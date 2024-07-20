
import asyncio
import logging

from aiogram import Bot, Dispatcher

from app import handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # Создание экземпляра бота
    bot = Bot(token="7299584966:AAGmsEIJyGoJe9xfJDABnDrOqp1GpJlx8K8")

    # Создание диспетчера
    dp = Dispatcher()

    # Включение роутеров
    dp.include_router(handlers.router)

    # Запуск поллинга
    try:
        await dp.start_polling(bot)
    finally:
        # Закрытие бота
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
