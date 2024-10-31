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

# Словари для хранения истории сообщений и состояния бота
user_histories = {}
user_states = {}

async def ask_gpt(user_id, text, temperature=0.3):
    try:
        if user_id not in user_histories:
            user_histories[user_id] = []

        user_histories[user_id].append({"role": "user", "content": text})

        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            messages=user_histories[user_id],
            temperature=temperature
        )

        if isinstance(response, str):
            bot_response = response
        else:
            bot_response = response['choices'][0]['message']['content']

        user_histories[user_id].append({"role": "assistant", "content": bot_response})
        return bot_response

    except Exception as e:
        logging.error(f"Error in ask_gpt: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса."

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = True  # Включаем генерацию по умолчанию
    await message.reply("Привет! Я Chat-GPT с памятью. Напиши что-нибудь!")

@dp.message(Command('off'))
async def turn_off(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = False  # Отключаем генерацию
    await message.reply("Бот отключен. Я не буду генерировать ответы.")

@dp.message(Command('on'))
async def turn_on(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = True  # Включаем генерацию
    await message.reply("Бот снова включен. Напиши что-нибудь!")

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text.lower()

    # Обрабатываем все остальные сообщения с помощью GPT
    if user_states.get(user_id, True):  # По умолчанию бот включен
        response = await ask_gpt(user_id, text)
        await message.reply(response)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
