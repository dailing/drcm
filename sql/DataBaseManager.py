import sqlite3
from hashlib import md5
import logging

class DataBaseManager():
	"""DataBase operation Manager"""
	def __init__(self, dbName):
		self.logger = logging.getLogger('root.dbmanager')
		self.dbName = dbName
		self.conn = sqlite3.connect(dbName, check_same_thread=False)

		self.createTableIfNotExist()

	def newInstance(self):
		return DataBaseManager(self.dbName)

	def newConnection(self):
		return sqlite3.connect(self.dbName)


	def getAllLocalOnlyImageData(self):
		sqlQuery = "select name, pid, isLeftEye, male, birthday, timeId, uuid, md5Sum, data from PatientInfo where uptoServer = 0"
		try:
			conn = sqlite3.connect(self.dbName)
			res = list(conn.execute(sqlQuery))
		except Exception as e:
			return []
		else:
			return res
		finally:
			conn.close()


	def createTableIfNotExist(self) :
		sqlCreateTabel = 'CREATE TABLE IF NOT EXISTS PatientInfo' \
			'(name TEXT NOT NULL,'\
			'pid char(4)     NOT NULL,'\
			'isLeftEye TINYINT NOT NULL,' \
			'male TINYINT NOT NULL,' \
			'birthday date NOT NULL, timeId timestamp not Null, uuid CHAR(40) NOT NULL, md5Sum CHAR(32) NOT NULL, data blob NOT NULL, upToServer TINYINT NOT NULL, UNIQUE(uuid))'
		c = self.conn.cursor()
		c.execute(sqlCreateTabel)
		self.conn.commit()

	def progress_handler(self):
		self.instructionCnt += 1
		self.logger.debug('db instruction {}'.format(self.instructionCnt))


	def getAllRows(self, reply):
		try:
			res = self.conn.execute("select upToServer, pid, timeId from PatientInfo order by timeId DESC")
			res = list(res)
		except Exception as e:
			self.logger.exception("query error")
			res = []
		finally :
			self.logger.debug('emit reply from getAllRows')
			reply.emit(res)

	def insertRecord(self, obj, reply):
		try:
			cursor = self.conn.cursor()
			sqlInsert = 'insert into PatientInfo (name, pid, isLeftEye, male, birthday, timeId, uuid, md5Sum, data, upToServer) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
			data = obj.getData()
			md5Sum = md5(data).hexdigest()
			self.logger.debug(type(data))
			cursor.execute(sqlInsert, (
				str(obj.getName()),
				str(obj.getPid()), obj.isLeftEye(),
				obj.isMale(),
				str(obj.getBirthday()), obj.getTimeId(), 
				str(obj.getUUID()), md5Sum, data, 0)
			)
			self.conn.commit()
		except Exception as e:
			self.logger.exception('sql error')
			reply.emit(False)
		else:
			reply.emit(True)


def main():
	pass


if __name__ == '__main__':
	main()
