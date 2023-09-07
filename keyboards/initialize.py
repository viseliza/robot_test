from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

class HomeKeyboard:
    def main():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        
        keyboard.add(
            KeyboardButton('👥 Выбор группы'), 
            KeyboardButton('🗓 Просмотр замен')
        )

        return keyboard