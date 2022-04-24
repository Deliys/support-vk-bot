import os
import pymorphy2
import json
import vk_api
import random
import time

token = '9c6830732d60debcae9d51c24daf14223c9f0e6c3c7e5f4325e67d8bce487895eea822e5ee302f75ee480'
vk = vk_api.VkApi(token=token)
vk._auth_token()



morph = pymorphy2.MorphAnalyzer()




filters = ["'",",",".",'[',']','{','}','(',")",
'«','»',"-",";"
]
filters_key_word = [
	"почему",'зачем'
]


#создание базы индексирования

with open("index.json", "w",encoding='utf-8') as file:
	data = {}
	json.dump(data, file, indent=4, ensure_ascii=False)


def index_gen_list(text,file_name):
	#создание файла со словами из ответов на фопрос и построение индексов
	if ("index.json" in os.listdir())== False:
		with open("index.json", "w",encoding='utf-8') as file:
			data = {}
			json.dump(data, file, indent=4, ensure_ascii=False)
	with open('index.json', 'r',encoding='utf-8') as fp:
		data = json.load(fp)

	for i in text.split():

		if (i in data)==False:
			data[i] = {}
			data[i][file_name] = 1

		else:
			if (file_name in data[i])== False:
				data[i][file_name] = 1
			else:
				data[i][file_name] = 1 +int(data[i][file_name])


			

	with open("index.json", "w",encoding='utf-8') as file:    
	   json.dump(data, file, indent=4, ensure_ascii=False)
	return data



#фильтры 

def anti_form(text):
	text_s = ''
	for i in text.split():
		p = morph.parse(i)[0]  
		p = p.normal_form 
		text_s =text_s +" "+ p 

	return text_s

def anti_simfol(text):

	for uu in filters:
		text = text.translate({ord(i): None for i in uu})

	return text


for i in os.listdir("file/"): 
	with open('file/'+i, "r",encoding='utf-8') as file:
		#print(file.read().lower().split())
		text = file.read().lower()
		text = anti_simfol(text)
		text = anti_form(text)
		index_gen_list(text , "file/"+i)

def anti_key_word(text):
	# for uu in filters_key_word:
	#   text = text.translate({ord(uu): None for i in uu})

	text = text.split()

	for word in text: 
		if word in filters_key_word:
			text.remove(word)

	text_s = ''
	for i in text:
		text_s = text_s + " "+i

	return text_s
#поисковик

def search(text):
	text = anti_simfol(text)
	text = anti_form(text)
	text = anti_key_word(text)


	text = text.split()

	index_stat = {}
	with open('index.json', 'r',encoding='utf-8') as fp:
		data = json.load(fp)
	for i in text :
		if (i in data) == True:
			for ii in data[i]:
				if (ii in index_stat)==True:
					index_stat[ii]['mass'] = index_stat[ii]['mass'] + data[i][ii]
					index_stat[ii]['v_mass'] = index_stat[ii]['v_mass'] +1
				else:
					index_stat[ii] = {}
					index_stat[ii]['mass'] =  data[i][ii]
					index_stat[ii]['v_mass'] = 1
	


	#поиск файлов с большим вхождения всех слов и удаления малых------------------------

	max_v_mass = 0
	for  i in index_stat:
		if max_v_mass<index_stat[ii]['v_mass']:
			max_v_mass = index_stat[ii]['v_mass']
	for  i in index_stat:
		if max_v_mass < index_stat[i]['v_mass']:
			del index_stat[i]


	#-------------

	if len(index_stat)>0:
		b_max = [0]
		for  i in index_stat:
			if index_stat[i]['mass']>b_max[0]:
				b_max = [index_stat[i]['mass'] , i]

		with open(b_max[1], 'r',encoding='utf-8') as fp:
			text = fp.read()
			return text
	else:
		return "нет ничего похожего на ответ"



#-----------------vk бот


while True:
	try:
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]
			vk.method("messages.send", {"peer_id": id, "message": search(body), "random_id": random.randint(1, 2147483647)})
	except Exception as E:
		time.sleep(1)




