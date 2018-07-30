import sqlite3
import logging

pip install pywifi==1.1.6

logger = logging.getLogger('root.wifiManager')
class wifiManager():
	"""manage wifi connection"""
	CUR_SSID = None
	SSID_MAP = {}
	initialized = False
	isConnecting = False
	def __init__(self):
		pass


	@staticmethod
	def initState():
		if wifiManager.initialized:
			return
		wifiManager.initialized = True
		logger.debug('init')
		sqlCreateTabel = 'CREATE TABLE IF NOT EXISTS wifiInfo' \
			'(ssid TEXT NOT NULL,'\
			'user TEXT   NOT NULL,'\
			'pwd TEXT NOT NULL, UNIQUE(ssid))'
		try:
			with sqlite3.connect('state.db') as conn:
				conn.execute(sqlCreateTabel)
		except Exception as e:
			logging.exeption("wifi init error")

		ssidQuerySql = "select * from wifiInfo"
		try:
			with sqlite3.connect('state.db') as conn:
				res = conn.execute(ssidQuerySql)
				for row in res:
					wifiManager.SSID_MAP[row[0]] = (row[1], row[2])
		except Exception as e:
			logging.exeption("wifi init error")

	@staticmethod
	def isConnected():
		return wifiManager.CUR_SSID != None

	@staticmethod
	def connectDefault():
		wifiManager.initState()
		wifiManager.isConnecting = True;

def main():
	print(wifiManager.isConnected())
	wifiManager.connectDefault()


if __name__ == '__main__':
	main()