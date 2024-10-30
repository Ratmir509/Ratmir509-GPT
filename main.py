import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import g4f

API_TOKEN = '8065495860:AAGhcgejUy2SPbVEpBp6GhBysfJ8gSINbDo'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def ask_gpt(text):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        # Проверяем, что ответ от g4f не пустой
        if isinstance(response, str):
            return response  # Если ответ строка, возвращаем его
        return response['choices'][0]['message']['content']  # Если это объект, получаем контент
    except Exception as e:
        logging.error(f"Error in ask_gpt: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса."

@dp.message(Command('start'))  # Используем Command для фильтра
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который поможет тебе. Напиши что-нибудь!")

@dp.message()  # Обрабатываем любые текстовые сообщения
async def handle_message(message: types.Message):
    text = message.text
    response = await ask_gpt(text)
    await message.reply(response)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
