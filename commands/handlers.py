from config import dp, bot
from config.config import DEBUG
from database import User, Group
from keyboards import HomeKeyboard
from docParse import parseDocument

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging

#logging.info("ok")

class Options(StatesGroup):
    enter_group = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    try:
        # Получаем пользователя
        user_id = message.chat.id
        
        # Дебаг при логгере
        #logging.info("ok")

        # Проверяем находится ли он в базе
        if not await User.get(user_id):
            # Добавляем пользователя
            await User.add(user_id)

        await bot.send_message(chat_id=user_id, text=f"Здравствуйте, {message.from_user.first_name}\nЯ предназначен для работы с сайтом novsu.ru для упрощения работы с сайтом.\n\nНа данный момент я могу:\nпросматривать существующие замены", reply_markup=HomeKeyboard.main())
    except Exception as error:
        print(f'[ Commands/Handlers/process_start_command ] Error: {error}')


# Обработка события нажатия на кнопку "Просмотр замен"
@dp.message_handler(Text(equals="🗓 Просмотр замен")) 
async def checkReplacement(msg: types.Message):
    await msg.answer(parseDocument('group'))


@dp.message_handler(Text(equals="👥 Выбор группы"), state=None) 
async def selectGroup(msg: types.Message):
    await Options.enter_group.set()
    await msg.reply('Введите номер группы', reply=False, reply_markup=types.ReplyKeyboardRemove())



# Запись полученного номера группы 
@dp.message_handler(state=Options.enter_group)
async def input_group(message: types.Message, state: FSMContext):
    #database.updateByQuery({"telegram_username": message.from_user.username }, {"telegram_username": message.from_user.username, "group": message.text})
    await message.answer('Номер группы успешно сохранен', reply=False, reply_markup=HomeKeyboard.main())
    await state.finish()