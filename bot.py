import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# ⚠️ Замените на токен, который выдал @BotFather
TOKEN = "5729872290:AAGoESQc6HkkFfNbbSsxrwDwjl64cO5Deco"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список шуточных фраз для поджопника
PHRASES = [
    " выдал мощный поджопник для ускорения 👟💥",
    " отправляет мотивирующий пинок под зад! 🦵✨ Быстрее!",
    " прописывает бодрящий поджопник. Работаем, ребята, работаем! 🏃‍♂️💨",
    " применил древнюю технику летящего тапка! 🩴☄️",
    " напоминает о дедлайне увесистым пинком! ⏰🔥"
]

@dp.message(Command("podzhopnik"))
async def give_kick(message: types.Message):
    # Проверяем, отправлена ли команда в ответ на другое сообщение
    if not message.reply_to_message:
        await message.reply(
            "Команду нужно вызывать **в ответе (reply)** на сообщение того, "
            "кому вы хотите дать поджопник! 😉", 
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Получаем имена отправителя и «жертвы»
    sender = message.from_user.mention_markdown(v=2)
    target = message.reply_to_message.from_user.mention_markdown(v=2)
    
    # Выбираем случайную фразу
    action = random.choice(PHRASES)
    
    # Формируем и отправляем сообщение
    text = f"{sender}{action} {target}"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

async def main():
    print("Бот запущен и готов раздавать пинки...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
