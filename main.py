import asyncio
import configparser

from tickets import get_tickets
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

config = configparser.ConfigParser()
config.read('config.ini')
api_token = config.get('token', 'token_api')

bot = Bot(token=api_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Сейчас я тебе покажу все абонементы FitnessHaus в Ярославле на текущий момент!")
    tickets_str = ''
    for ticket in sorted(get_tickets(), key=lambda ticket: ticket['price_on_month']):
       tickets_str += "{}\nСроком на {}\n{}р\n{:.2f}р за месяц\n\n".format(ticket['name'], ticket['time'],  ticket['price'],  ticket['price_on_month'])
    tickets_str += "https://market.fitnesshouse.ru/jar"
    await bot.send_message(chat_id=message.from_user.id, text=tickets_str)
    
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())