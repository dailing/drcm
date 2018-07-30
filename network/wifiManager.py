import sqlite3
import logging
#https://wifi.readthedocs.io/en/latest/scanning.html
from wifi import Cell, Scheme

logger = logging.getLogger('root.wifiManager')
class wifiManager():
	"""manage wifi connection"""
	CUR_SSID = None
	CELLS = None
	isConnecting = False
	def __init__(self):
		pass


	@staticmethod
	def getWifiList():
		wifiManager.CELLS = Cell.all('wlan0')
		return [(c.quality, c.ssid, '******' if Scheme.find('wlan0', c.ssid) is not None else '------') for c in wifiManager.CELLS]

	@staticmethod
	def isConnected():
		return wifiManager.CUR_SSID != None

	@staticmethod
	def connectDefault():
		if wifiManager.CELLS is None:
			wifiManager.getWifiList()
		interface = 'wlan0'
		wifiManager.isConnecting = True
		cells = wifiManager.CELLS
		for c in cells:
			scheme = Scheme.find(interface, c.ssid)
			if scheme is not None:
				try:
					scheme.activate()
				except Exception as e:
					continue
				else :
					break
		wifiManager.isConnecting = False

	@staticmethod
	def connectWifi(ssid, pwd):
		if wifiManager.CELLS is None:
			wifiManager.getWifiList()
		for c in wifiManager.CELLS :
			if c.ssid == ssid:
				try:
					scheme = Scheme.for_cell('wlan0', ssid, c, pwd)
					scheme.activate()
				except Exception as e:
					raise e
					return False
				else :
					scheme.save()
					return True

def main():
	print(wifiManager.connectWifi('sbsbsbs', '12345678'))


if __name__ == '__main__':
	main()