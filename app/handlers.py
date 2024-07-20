
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

import app.keyboard as kb
from app.Get_jokes import get_joke
from app.sql import write_grade, read_jokes_from_sqlite

# привет


# подключение роутера
router = Router()

# ответ на команду /start


@router.message(F.text == '/start')
async def start(message: Message):
    await message.answer("Привет, я могу рассказать анекдот, а ты его оценишь!", reply_markup=kb.main)

# вызов функции get_joke и отправка анекдота


@router.message(F.text == 'Анекдот')
async def get_joke_handler(message: Message):
    try:
        joke = get_joke()
        await message.answer(joke, reply_markup=kb.handlers_grade)
        return joke
    except TypeError as e:
        await message.answer("Произошла ошибка при получении анекдота.")
        print(f"Error: {e}")


# получение оценки от пользователя и запись в базу
@router.callback_query(F.data)
async def get_grade(callback: CallbackQuery):
    try:
        grade = int(callback.data)
        await callback.answer("Сохранено")
        joke = callback.message.text
        await write_grade(joke, grade)
        print("Записано")

        # Удаляем кнопки
        await callback.message.edit_reply_markup(reply_markup=None)

        # Отправляем новый анекдот
        new_joke = get_joke()
        await callback.message.answer(new_joke, reply_markup=kb.handlers_grade)
    except ValueError as e:
        await callback.answer("Некорректная оценка.")
        print(f"Error: {e}")


# функция для получения лидеров
# функция для получения лидеров
@router.message(F.text == 'Лидеры')
async def get_leaderboard(message: Message):
    try:
        leaderboard = await read_jokes_from_sqlite()
        if leaderboard:
            leaderboard_sorted = sorted(leaderboard, key=lambda x: x[3], reverse=True)  # сортировка по оценкам
            top_three_jokes = leaderboard_sorted[:3]  # выбор трёх анекдотов с высшим баллом
            leaderboard_text = "\n".join([f"{joke[0]} (Оценка: {joke[3]})" for joke in top_three_jokes])
            print(leaderboard_text)
            await message.answer("Топ 3 анекдота с высшим баллом:\n" + leaderboard_text)
        else:
            await message.answer("Нет анекдотов с двумя оценками.")
    except Exception as e:
        await message.answer("Произошла ошибка при получении лидеров.")
        print(f"Error: {e}")

