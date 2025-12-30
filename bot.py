import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# === НАСТРОЙКИ ===
API_TOKEN = "8398790961:AAFiGuqqyKAQPOGilxT0woGQeP3N0I-1PZE"
CHANNEL_ID = -1002053303824        # ID закрытого канала
CHANNEL_LINK = "https://t.me/+g2DGQKhjuUA4Mzhi"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# === ПРОВЕРКА ПОДПИСКИ ===
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

# === КНОПКИ ПОДПИСКИ ===
def subscribe_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="check_sub")]
    ])

# === /start ===
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer(
            "Чтобы узнать код, подпишитесь на данные каналы.",
            reply_markup=subscribe_keyboard()
        )
        return

    await message.answer("✅ Подписка подтверждена.\nСкиньте код.")

# === КНОПКА «ПРОВЕРИТЬ ПОДПИСКУ» ===
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub_handler(callback: types.CallbackQuery):
    if await check_subscription(callback.from_user.id):
        await callback.message.answer(
            "✅ Подписка подтверждена.\nСкиньте код."
        )
    else:
        await callback.message.answer(
            "⏳ Заявка отправлена.\n"
            "Ожидайте подтверждения (обычно до 2 минут),\n"
            "затем нажмите «Проверить подписку» снова."
        )
    await callback.answer()

# === ОБРАБОТКА КОДА ===
@dp.message(lambda m: not m.text.startswith("/"))
async def code_handler(message: types.Message):
    code = message.text.strip()

    await message.answer("🔍 Ищу…")
    await asyncio.sleep(2)

    await message.answer(
        "🎬 Код найден ✅\n"
        "Фильм или сериал будет отправлен."
    )

# === ЗАПУСК ===
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
