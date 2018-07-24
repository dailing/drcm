import sqlite3
from hashlib import md5

class DataBaseManager():
	"""DataBase operation Manager"""
	def __init__(self, dbName):
		super(DataBaseManager, self).__init__()
		self.dbName = dbName
		self.conn = sqlite3.connect(dbName)
		self.createTableIfNotExist()


	def createTableIfNotExist(self) :
		sqlCreateTabel = 'CREATE TABLE IF NOT EXISTS PatientInfo' \
			'(name TEXT NOT NULL,'\
			'pid INT     NOT NULL,'\
			'isLeftEye TINYINT NOT NULL,' \
			'male TINYINT NOT NULL,' \
			'birthday date NOT NULL, timeId timestamp not Null, uuid CHAR(40) NOT NULL, md5Sum CHAR(32) NOT NULL, data blob NOT NULL, UNIQUE(uuid))'
		c = self.conn.cursor()
		c.execute(sqlCreateTabel)
		self.conn.commit()

	def insertRecord(self, obj, reply):
		try:
			cursor = self.conn.cursor()
			sqlInsert = 'insert into PatientInfo (name, pid, isLeftEye, male, birthday, timeId, uuid, md5Sum, data) values(?, ?, ?, ?, ?, ?, ?, ?, ?)'
			data = obj.getData()
			md5Sum = md5(data).hexdigest()
			cursor.execute(sqlInsert, (
				obj.getName(),
				obj.getPid(), obj.isLeftEye(),
				obj.isMale(),
				obj.getBirthday(), obj.getTimeId(), 
				str(obj.getUUID()), md5Sum, data)
			)
			self.conn.commit()
		except Exception as e:
			print(e, 'sql error')
			reply.emit(False)
		else:
			reply.emit(True)
		

