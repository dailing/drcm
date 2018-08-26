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


	def getDataForUpload(self):
		sqlQuery = "select name, pid, isLeftEye, male, birthday, timeId, uuid, md5Sum, data from PatientTalbe as pt, ImageTable as it where it.uptoServer = 0 AND it.pid = pt.pid"
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
		PatientTalbe = 'CREATE TABLE IF NOT EXISTS PatientTalbe' \
		'(name TEXT NOT NULL,'\
			'pid char(4)     NOT NULL,'\
			'male TINYINT NOT NULL,' \
			'created date NOT NULL,' \
			'UNIQUE(pid))'
		c = self.conn.cursor()
		c.execute(PatientTalbe)
		self.conn.commit()
		ImageTable = 'CREATE TABLE IF NOT EXISTS ImageTable' \
			'(pid char(4)     NOT NULL,'\
			'isLeftEye TINYINT NOT NULL,' \
			'timeId timestamp not Null, uuid CHAR(40) NOT NULL, md5Sum CHAR(32) NOT NULL, data blob NOT NULL, upToServer TINYINT NOT NULL, UNIQUE(uuid))'
		c = self.conn.cursor()
		c.execute(ImageTable)
		self.conn.commit()

	def progress_handler(self):
		self.instructionCnt += 1
		self.logger.debug('db instruction {}'.format(self.instructionCnt))


	def getPatientList(self, reply):
		try:
			res = self.conn.execute("select male, name, pid, created from PatientTalbe order by created DESC")
			res = list(res)
		except Exception as e:
			self.logger.exception("query error")
			res = []
		finally :
			self.logger.debug('emit reply from getAllRows')
			reply.emit(res)

	def getPatientImages(self, pid, reply):
		try:
			res = self.conn.execute("select data from ImageTable where pid = ? order by timeId DESC", pid)
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
			sqlInsert = 'insert into PatientInfo (name, pid, male, created) values(?, ?, ?, ?)'
			data = obj.getData()
			md5Sum = md5(data).hexdigest()
			self.logger.debug(type(data))
			cursor.execute(sqlInsert, (
				str(obj.getName()),
				str(obj.getPid()),
				obj.isMale(),
				str(obj.getCreatedTime()))
			)
			self.conn.commit()
		except Exception as e:
			self.logger.exception('sql error')
			reply.emit(False)
		else:
			reply.emit(True)

	def insertData(self, obj, reply):
		try:
			cursor = self.conn.cursor()
			sqlInsert = 'insert into ImageTable (pid, isLeftEye, timeId, uuid, md5Sum, data, upToServer) values(?, ?, ?, ?, ?, ?, ?)'
			data = obj.getData()
			md5Sum = md5(data).hexdigest()
			self.logger.debug(type(data))
			cursor.execute(sqlInsert, (
				str(obj.getPid()), obj.isLeftEye(),
				obj.getTimeId(), 
				str(obj.getUUID()), md5Sum, data, 0)
			)
			self.conn.commit()
		except Exception as e:
			self.logger.exception('sql error')
			reply.emit(False)
		else:
			reply.emit(True)


def main():
	dbm = DataBaseManager('test.db')


if __name__ == '__main__':
	main()
