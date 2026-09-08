import asyncio
import random
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# ⚠️ Вставьте сюда ваш токен от @BotFather вместо текста ниже!
TOKEN = "5729872290:AAGoESQc6HkkFfNbbSsxrwDwjl64cO5Deco"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список шуточных фраз
PHRASES = [
    " выдал мощный поджопник для ускорения 👟💥",
    " отправляет мотивирующий пинок под зад! 🦵✨ Быстрее!",
    " прописывает бодрящий поджопник. Работаем, ребята, работаем! 🏃‍♂️💨",
    " применил древнюю технику летящего тапка! 🩴☄️",
    " напоминает о дедлайне увесистым пинком! ⏰🔥"
]

# Общая функция для отправки поджопника
async def send_kick(message: types.Message):
    # Используем mention_html(), чтобы избежать багов с разметкой
    sender = message.from_user.mention_html()
    target = message.reply_to_message.from_user.mention_html()
    
    action = random.choice(PHRASES)
    text = f"{sender}{action} {target}"
    
    # Отправляем сообщение в формате HTML
    await message.answer(text, parse_mode=ParseMode.HTML)

# 1. Реагируем на команду /podzhopnik в ответе на сообщение
@dp.message(Command("podzhopnik"))
async def give_kick_command(message: types.Message):
    if not message.reply_to_message:
        await message.reply(
            "Команду нужно вызывать в ответе (reply) на сообщение того, "
            "кому вы хотите дать поджопник! 😉"
        )
        return
    await send_kick(message)

# 2. Автоматически ловим имена Герман, Гера, Гермиона в ответах
@dp.message()
async def check_names(message: types.Message):
    if message.reply_to_message and message.text:
        text_lower = message.text.lower()
        trigger_words = ["герман", "гера", "гермиона"]
        
        if any(word in text_lower for word in trigger_words):
            await send_kick(message)

# Микро-сервер для обмана портов Render (чтобы бот не падал)
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

async def main():
    # Запускаем микро-сервер в отдельном потоке
    threading.Thread(target=run_dummy_server, daemon=True).start()
    print("Бот успешно запущен и слушает чат...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
