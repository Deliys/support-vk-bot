class user(object):
	"""docstring for user"""

	def create_user(self):
		self.base.cur.execute("""SELECT role
			   FROM users
			   WHERE type=? and id_from=?
				   """,(self.type_s,self.id))
		result = self.base.cur.fetchone() 
		if (not result):
			self.base.cur.execute("INSERT INTO users VALUES (NULL,?, ? ,?,?)", (1, self.type_s,self.id ,self.role))
			self.base.conn.commit()
		else:	
			self.role = result[0]

	def add(self,text):
		if self.role in ["admin"]:
			if len(list(text[5:]))>0:

				self.base.add_questions(text[5:])
				return "вопрос добавлен"
			else:
				return "кроме команды ничего нет"
		else:
			return "недостаточно прав"
	def delete(self,text):
		if self.role in ["admin"]:
			if len(list(text[8:]))>0:
				if  (not text[8:].isdigit()):
					return "не числовой тип .\n введите /list"
				else:
					if self.base.delete_questions(int(text[8:])):
						return "успешно удалено"	
					else:
						return "нет такого индекса \nвведите /list"
				#self.base.add_questions(text[8:])
				
			else:
				return "кроме команды ничего нет"
		else:
			return "недостаточно прав"

	def list(self):
		if self.role in ["admin"]:
			return self.base.list_short_que()
		else:
			return "недостаточно прав"
		
	def help(self):
		text = "/list\n/add\n/delete\n"
		return text
	def __init__(self, id , type_s  , base):

		super(user, self).__init__()
		self.id = id
		self.type_s = type_s
		self.role = "user"
		self.base = base
		self.create_user()

		


		