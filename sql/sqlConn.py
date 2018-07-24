#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, date
class SqlConn():
	"""sql operation wrapper"""
	def __init__(self, db):
		super(SqlConn, self).__init__()
		self.db = db
		self.conn = sqlite3.connect(self.db)
		SqlConn.createTabelIfNotExist(self.conn)
		SqlConn.queryTable(self.conn)


	def __enter__(self):
		return self

	def __exit__(self, mtype, value, trace):
		print(mtype, value, trace)
		self.conn.close()

	def insertValues(self, values):
		c = self.conn.cursor()
		sqlShowTables = "insert into PatientInfo(name, pid, isLeftEye, male, birthday, timeId, uuid) "\
		"values (?,?,?,?,?,?,?)"
		c.execute(sqlShowTables, values)
		
		self.conn.commit()


	@staticmethod
	def queryTable(conn):
		c = conn.cursor()
		# query = "SELECT name FROM sqlite_master WHERE type='table';"
		query = "select * from PatientInfo";
		c.execute(query)
		conn.commit()
		for res in c:
			print(res)

	@staticmethod
	def createTabelIfNotExist(conn):
		c = conn.cursor()
		sqlCreateTabel = 'CREATE TABLE IF NOT EXISTS PatientInfo' \
			'(name TEXT NOT NULL,'\
			'pid INT     NOT NULL,'\
			'isLeftEye TINYINT NOT NULL,' \
			'male TINYINT NOT NULL,' \
			'birthday date NOT NULL, timeId timestamp not Null, uuid CHAR(40) NOT NULL)'
		c.execute(sqlCreateTabel)
		conn.commit()

	def close(self):
		self.conn.close()

def SqlConnTestDriver():
	
	with SqlConn('test1.db') as sqlObj:
		sqlObj.insertValues(("str", 143, True, True, '2018-07-24', 1, '863b2224-bde6-475d-a8d8-104b137b7a35'))
		SqlConn.queryTable(sqlObj.conn)


if __name__ == '__main__':
	SqlConnTestDriver()