import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3

"""
изменение:
1: поддержка тг 
2: добавление вопросов в базу с разу из бота
3: поиск релевантного ответа передано библиотеке nltk и sklearn 
(внутри работает как векторизация текста)

"""


# загрузка массива состоящего из статей из базы
class base(object):
	def cheak_update(self):#просто сравнивает версию кешированой таблицы с файловой версией
		#нужно для того что вк и тг версии правильно синхронили список вопросов
		#print(self.cur.execute("SELECT * FROM 'service table';").fetchall())
		
		if self.vers != self.cur.execute("SELECT * FROM 'service table';").fetchall()[0][1]:
			self.vers =self.cur.execute("SELECT * FROM 'service table';").fetchall()[0][1]
			self.questions = self.get_questions()#обновление переменной статей


	def add_questions(self , text):
		self.cur.execute("INSERT INTO questions VALUES (NULL, ? ,?)", ("", text))
		self.conn.commit()
	def delete_questions(self , id_t):
		self.cur.execute("""SELECT id
			   FROM questions
			   WHERE id=?
				   """,(id_t,))
		result = self.cur.fetchone() 

		if (result):
			self.cur.execute("DELETE FROM questions WHERE id=?", (id_t,))
			self.conn.commit()
			return True
		else:
			return False
	def list_short_que(self):
		text = ""
		#нужно для вывода короткого варианта вопроса перед удалением
		for i in self.cur.execute("""SELECT * from questions""").fetchall(): 
			ii =  (i[2][:20] + '..') if len(i[2]) > 20 else i[2]
			text+="[{}] {}\n".format(i[0],ii)
		return text
	def get_request(self , que):
		# преобразование текста в матрицу TF-IDF
		vectorizer = TfidfVectorizer()
		tfidf = vectorizer.fit_transform(self.questions)

		# получение списка статей, соответствующих запросу
		query_vec = vectorizer.transform([que])
		results = (tfidf * query_vec.T).toarray()
		indices = results.argsort(axis=0)[::-1]

		return self.questions[indices[0][0]]
	def get_questions(self):
		self.cur.execute("SELECT text_que FROM questions;")
		three_results = self.cur.fetchall()
		a = []
		for i in three_results:
			a.append(i[0])
		return a 

	def __init__(self):
		super(base, self).__init__()
		
		#подключение bd----------------
		conn = sqlite3.connect('main.db')
		self.conn = conn
		self.cur = conn.cursor()

		self.cur.execute('''CREATE TABLE IF NOT EXISTS log (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	user_id INTEGER,
    	que_id  INTEGER,
    	text    TEXT
		);''')


		self.cur.execute('''CREATE TABLE IF NOT EXISTS questions (
  		id  INTEGER PRIMARY KEY AUTOINCREMENT,
   		name STRING,
    	text_que STRING
		);
		''')


		self.cur.execute('''CREATE TABLE IF NOT EXISTS [service table] (
    	id,
    	update_version INTEGER
		);''')


		self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
    		id       INTEGER PRIMARY KEY,
    		math_msg INTEGER,
    		type     TEXT,
    		id_from  INTEGER,
    		role     TEXT
			);
			''')



		self.conn.commit()

		if self.cur.execute("SELECT * FROM 'service table';").fetchone() == None:
			self.vers = 0
		else:
			self.vers =self.cur.execute("SELECT * FROM 'service table';").fetchone()[0][1]
		
		#массив статей
		self.questions = self.get_questions()

