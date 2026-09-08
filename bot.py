import asyncio
import random
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# ⚠️ Вставьте ваш токен от @BotFather
TOKEN = "5729872290:AAGoESQc6HkkFfNbbSsxrwDwjl64cO5Deco"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Шуточные фразы
PHRASES = [
    " выдал мощный поджопник для ускорения 👟💥",
    " отправляет мотивирующий пинок под зад! 🦵✨ Быстрее!",
    " прописывает бодрящий поджопник! 🏃‍♂️💨",
    " применил древнюю технику летящего тапка! 🩴☄️",
    " поджопник! ⏰🔥"
    "5 бокалов пива и один поджопник сэр!"
]

# 1. Команда /podzhopnik в режиме Ответа (Reply)
@dp.message(Command("podzhopnik"))
async def give_kick_command(message: types.Message):
    # Более надежная проверка на ответ (отлавливает любые типы reply)
    if message.reply_to_message is not None:
        sender = message.from_user.mention_html()
        target = message.reply_to_message.from_user.mention_html()
        action = random.choice(PHRASES)
        
        await message.answer(f"{sender}{action} {target}", parse_mode=ParseMode.HTML)
    else:
        await message.reply(
            "Команду нужно вызывать в ответе (reply) на сообщение того, "
            "кому вы хотите дать поджопник! 😉"
        )

# 2. Авто-реагирование на имена (РАБОТАЕТ ВСЕГДА, даже без Reply!)
@dp.message()
async def check_names(message: types.Message):
    if not message.text:
        return
        
    text_lower = message.text.lower()
    trigger_words = ["герман", "гера", "гермиона"]
    
    # Если кто-то написал это имя в чате
    if any(word in text_lower for word in trigger_words):
        action = random.choice(PHRASES)
        
        # Если это было сделано в ответе — пинаем того, НА КОГО ответили
        if message.reply_to_message is not None:
            sender = message.from_user.mention_html()
            target = message.reply_to_message.from_user.mention_html()
            await message.answer(f"{sender}{action} {target}", parse_mode=ParseMode.HTML)
        # Если просто написали в чат — бот в шутку пинает САМОГО отправителя за упоминание Германа!
        else:
            sender = "Система правосудия 🤖"
            target = message.from_user.mention_html()
            await message.answer(f"{sender}{action} {target} за упоминание запретного имени! 🤫", parse_mode=ParseMode.HTML)

# Заглушка портов для Render
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

async def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()
    print("Бот успешно запущен и готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
