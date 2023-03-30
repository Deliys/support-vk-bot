
import base
from user import user as USER
from vkbottle.bot import Bot , Message
from vkbottle import Keyboard ,KeyboardButtonColor ,Text , OpenLink , EMPTY_KEYBOARD


		
b = base.base() #объект для общение с базой




bot = Bot(token="")

@bot.on.message()
async def message_handler(message:Message):		
	
	user = USER(message.from_id , "vk" , b)

	if (message.text.lower() == 'привет'):
		await message.answer("напиши свой вопрос")	


	elif message.text.lower().split()[0] == "/add":
		await message.answer(user.add(message.text.lower()))	

		
	elif message.text.lower().split()[0] == "/delete":
		await message.answer(user.delete(message.text.lower()))	

	elif message.text.lower().split()[0] == "/list":
		await message.answer(user.list())	

	elif message.text.lower().split()[0] == "/help":
		await message.answer(user.help())	

	else:
		await message.answer(b.get_request(message.text.lower()))	
	
bot.run_forever()