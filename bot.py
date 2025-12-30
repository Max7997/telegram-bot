import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= НАСТРОЙКИ =================

API_TOKEN = os.getenv("BOT_TOKEN")  # токен берётся из Railway Variables

CHANNEL_ID = -1002053303824        # ID закрытого канала
CHANNEL_LINK = "https://t.me/+g2DGQKhjuUA4Mzhi"

# ================= ИНИЦИАЛИЗАЦИЯ =================

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ================= ПРОВЕРКА ПОДПИСКИ =================

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

# ================= КНОПКИ =================

def subscribe_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📢 Подписаться на канал",
            url=CHANNEL_LINK
        )],
        [InlineKeyboardButton(
            text="🔄 Проверить подписку",
            callback_data="check_sub"
        )]
    ])

# ================= /start =================

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer(
            "Чтобы получить код, подпишитесь на канал 👇",
            reply_markup=subscribe_keyboard()
        )
        return

    await message.answer(
        "✅ Подписка подтверждена!\n\n"
        "Теперь отправьте код."
    )

# ================= ПРОВЕРИТЬ ПОДПИСКУ =================

@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub_handler(callback: types.CallbackQuery):
    if await check_subscription(callback.from_user.id):
        await callback.message.answer(
            "✅ Подписка подтверждена!\n\n"
            "Теперь отправьте код."
        )
    else:
        await callback.message.answer(
            "⏳ Вы ещё не подписаны.\n\n"
            "Если заявка отправлена — подождите пару минут и нажмите кнопку снова."
        )

    await callback.answer()

# ================= ОБРАБОТКА КОДА =================

@dp.message(lambda m: m.text and not m.text.startswith("/"))
async def code_handler(message: types.Message):
    code = message.text.strip()

    await message.answer("🔍 Проверяю код…")
    await asyncio.sleep(2)

    # Тут позже можно сделать реальную проверку кода
    await message.answer(
        "🎬 Код найден ✅\n\n"
        "Фильм или сериал будет отправлен."
    )

# ================= ЗАПУСК =================

async def main():
    if not API_TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден. Добавь его в Railway Variables.")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
