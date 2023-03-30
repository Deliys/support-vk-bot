
import base
from user import user as USER

import logging
from aiogram import Bot as BBot
from aiogram import Dispatcher, executor, types
from aiogram.types import CallbackQuery, Message,\
	InlineKeyboardButton, InlineKeyboardMarkup

# Объект бота
bot = BBot(token="")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
b = base.base() #объект для общение с базой




@dp.message_handler()
async def any_text_message2(message: types.Message):
	
	user = USER(message.from_user.id , "tg" , b)

	if (message.text.lower() == 'привет'):
		await bot.send_message(
		chat_id=message.from_user.id,
		text='напиши свой вопрос')

	elif message.text.lower().split()[0] == "/add":
		
		await bot.send_message(
		chat_id=user.id,
		text=user.add(message.text.lower()))
	elif message.text.lower().split()[0] == "/delete":
		await bot.send_message(
		chat_id=user.id,
		text=user.delete(message.text.lower()))
	elif message.text.lower().split()[0] == "/list":
		await bot.send_message(
		chat_id=user.id,
		text=user.list())
	elif message.text.lower().split()[0] == "/help":
		await bot.send_message(
		chat_id=user.id,
		text=user.help())
	else:
		await bot.send_message(
		chat_id=message.from_user.id,
		text=b.get_request(message.text.lower()))
	
executor.start_polling(dp, skip_updates=True)