from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Анекдот")],
        [KeyboardButton(text="Лидеры")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Давай оценивать..."
)
