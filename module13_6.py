from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
button2 = InlineKeyboardButton(text="Формулы расчёта", callback_data='formulas')
kb.add(button)
kb.add(button2)

start_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
            KeyboardButton(text='Расчитать'),
            KeyboardButton(text='Информация')
            ]
        ],
        resize_keyboard=True
    )


@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer("Выберите опцию: ", reply_markup=kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("10 x вес(кг) + 6,25 x рост(см) - 5 x возраст (г) - 161")

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Сколько вам лет?")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Какой ваш рост?")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Какой ваш вес?")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data["age"])
    growth = float(data["growth"])
    weight = float(data["weight"])

    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f'Ваша норма калорий = {calories:.2f}')


#@dp.callback_query_handler(text = 'info')
#async def infor(call):
    #await call.message.answer("Информация о боте")
    #await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
