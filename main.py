from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


import logging
import asyncio
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random

# Initialize bot and dispatcher separately
bot = Bot(token="7767862398:AAF0LhDZ6gN3b-mZOKpsw0x2YTPW1sknQdo")
dp = Dispatcher()  # No bot argument needed

class Test(StatesGroup):
    test = State()

@dp.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привет")
    await asyncio.sleep(0.3)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="да")]],
        resize_keyboard=True
    )
    await message.answer("Начнем, да?", reply_markup=keyboard)
    await state.set_state(Test.test)

@dp.message(Test.test, F.text.lower() == "да")
async def start_test(message: Message, state: FSMContext):
    await message.answer("Отлично!",reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(0.3)
    await message.answer("1")
    await asyncio.sleep(1)
    await message.answer("2")
    await asyncio.sleep(1)
    await message.answer("3")
    await asyncio.sleep(1)
    
    x = random.randint(1, 1000)
    y = random.uniform(0, 1)
    result = x * y
    await message.answer(f"Сколько будет {x} * {y:.2f}?")
    await state.update_data({"result": result})

@dp.message(Test.test, F.text.lower() != "exit")
async def check_answer(message: Message, state: FSMContext):
    try:
        user_answer = float(message.text)
        data = await state.get_data()
        correct_answer = data.get("result", 0)
        
        if abs(user_answer - correct_answer) < 0.01:
            await message.answer("Вы ответили правильно!")
        else:
            await message.answer(f"Вы ответили неправильно! Правильный ответ: {correct_answer:.2f}")
        
        x = random.randint(1, 1000)
        y = random.uniform(0, 1)
        result = x * y
        await message.answer(f"Сколько будет {x} * {y:.2f}?")
        await state.update_data({"result": result})
        
    except ValueError:
        await message.answer("Пожалуйста, введите число.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)  # Pass bot instance to start_polling

if __name__ == "__main__":
    asyncio.run(main())