from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = '...'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState():

    age = State()
    growth = State()
    weight = State()


    @dp.message_handler(text = 'Calories')
    async def set_age(message):
        await message.answer('Введите свой возраст.')
        await UserState.age.set()


    @dp.message_handler(state = UserState.age)
    async def set_growth(message, state):
        await state.update_data(age = message.text)
        await message.answer(f'Введите свой рост')
        await UserState.growth.set()


    @dp.message_handler(state = UserState.growth)
    async def set_weight(message, state):
        await state.update_data(growth = message.text)
        await message.answer(f'Введите свой вес')
        await UserState.weight.set()

    @dp.message_handler(state = UserState.weight)
    async def send_calories(message, state):
        data = state.get_data()
        await state.update_data(weight = message.text)
        data = state.get_data()
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
        await state.finish()
        await message.answer(f'Ваша норма калорий: {calories}')

    if __name__ == '__main__':
        executor.start_polling(dp,skip_updates=True)