from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import asyncio

api = "7545702137:AAFmT_fwP09R5q35yTR0VgMvrL55nQMYKCQ"
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = 'Calories')
async def set_age(message):
    await message.answer("Сколько вам лет?")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Какой ваш рост?")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Какой ваш вес?")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()

    age = int(data["age"])
    growth = float(data["growth"])
    weight = float(data["weight"])

    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f'Ваша норма калорий = {calories:.2f}')






if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)