import asyncio
import logging
from decouple import config
from get_weather import get_weather_text

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = config('token', default='')
cities = {
    "Москва": "moscow-4368",
    "Санкт-Петербург": "sankt-peterburg-4079",
    "Сочи": "sochi-5233",
    "Ростов": "rostov-na-donu-5110",
}

router = Router()


def keyboard_weather():
    keyboard_builder = InlineKeyboardBuilder()
    for i in cities.keys():
        keyboard_builder.button(text=i, callback_data=cities[i])
    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()

@router.message(Command("weather"))
async def info_weather(message: types.Message):
    await message.answer("Выберите город.", reply_markup=keyboard_weather())

@router.callback_query()
async def getting_weather(call: types.CallbackQuery):
    await call.answer()
    city = call.data
    text = await get_weather_text(city=city)
    await call.message.edit_text(text=text, reply_markup=keyboard_weather())


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())