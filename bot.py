import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

# ⚠️ Не забудьте вставить ваш токен от @BotFather!
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
    sender = message.from_user.mention_markdown(v=2)
    target = message.reply_to_message.from_user.mention_markdown(v=2)
    action = random.choice(PHRASES)
    text = f"{sender}{action} {target}"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# 1. Реагируем на стандартную команду /podzhopnik (обязательно в ответе на сообщение)
@dp.message(Command("podzhopnik"))
async def give_kick_command(message: types.Message):
    if not message.reply_to_message:
        await message.reply(
            "Команду нужно вызывать **в ответе (reply)** на сообщение того, "
            "кому вы хотите дать поджопник! 😉", 
            parse_mode=ParseMode.MARKDOWN
        )
        return
    await send_kick(message)

# 2. Автоматически ловим имена Герман, Гера, Гермиона (тоже работает ТОЛЬКО если это ответ на чьё-то сообщение)
@dp.message()
async def check_names(message: types.Message):
    # Проверяем, что это ответ на сообщение и в тексте есть нужные имена
    if message.reply_to_message and message.text:
        text_lower = message.text.lower()
        trigger_words = ["герман", "гера", "гермиона"]
        
        # Если хотя бы одно слово совпало
        if any(word in text_lower for word in trigger_words):
            await send_kick(message)

# Фикс портов для Render (чтобы бот не отключался)
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

async def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()
    print("Бот запущен и готов раздавать пинки за имена...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
