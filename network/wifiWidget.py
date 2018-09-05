import sys
import logging
import subprocess
from subprocess import Popen, PIPE
import socket
from PyQt4 import QtGui, QtCore

from wifiManager import wifiManager
from utils.icons import get_icon
try:
	from sql.RunnableFunc import RunnableFunc
	from sql.PoolWrapper import PoolWrapper
except Exception as e:
	pass

from widget.LineEditDialog import LineEditDialog

def showKeyBoard():
	try:
		subprocess.Popen(["matchbox-keyboard"])
	except FileNotFoundError:
		pass
def hideKeyBoard():
	pass
	subprocess.Popen(["killall","matchbox-keyboard"])

def get_host_ip():
	"""
	enqury machine ip address
	:return: ip
	"""
	try:
		process = Popen(['ip','addr','show'],stdout=PIPE)
		olines = process.stdout.read().splitlines()
		addresses = []
		for line in olines:
			line = line.strip()
			if line.startswith('inet '):
				line = line.split()[1]
				addresses.append(line)
	except Exception as e :
		print(e)
		return 'None'
	return '\n'.join(addresses[1:])

def visulizeSignal(wifiData):
	#convert to percentage representation
	quality = wifiData[0].split('/')
	quality = float(quality[0]) / float(quality[1])
	quality = int(quality * 100)

	#'|' denote ten percent, '.' denote five percent
	rem = (quality % 10) > 5
	strQuality = '|' * (quality // 10) + ('|' if rem else '.')
	res = ['' if e is None else e for e in wifiData]
	print (strQuality)
	res[0] = strQuality
	return res


class WifiTableView(QtGui.QTableWidget):
	"""wifi mananger table list view"""

	wifiQuerySignal = QtCore.pyqtSignal(list)
	back_clicked = QtCore.pyqtSignal(name='back_clicked()')

	def __init__(self):
		QtGui.QTableWidget.__init__(self)
		self.pw = PoolWrapper()
		try:
			self.initTable()
		except Exception as e:
			print(e)
		self.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)

	def refresh_clicked(self):
		ipaddr = get_host_ip()
		print (ipaddr)

	@property
	def custom_right_header(self):
		right_header = get_icon('refresh')
		right_header.mouseReleaseEvent = lambda event:self.refresh_clicked()
		return right_header

	@property
	def custom_left_header(self):
		left_header = get_icon('back')
		left_header.mouseReleaseEvent = lambda event:self.back_clicked.emit()
		return left_header
		
	def tabCellClicked(self, i, j):
		if j != 1: # 
			return
		ssid = str(self.item(i, j).text())
		if ssid == self.wifiManager.getCurrentWifi():
			print ('is connected')
			return

		pwd = str(self.item(i, 2).text())
		pwd, isOkay = LineEditDialog.newInstance('password',pwd)
		if not isOkay:
			return
		self.item(i, 2).setText(pwd)
		if pwd == '******':
			pwd = None
		pwd = self.pw.start(
				RunnableFunc(
					self.wifiManager.connectWifi,
					ssid,
					pwd
				)
			)
		print(str(self.item(i, 2).text()))

	def initTable(self):
		self.wifiManager = wifiManager()
		# table.itemClicked.connect(self.tabItemDoubleClicked)
		self.cellClicked.connect(self.tabCellClicked)
		# tableItem 	= QtGui.QTableWidgetItem()
		self.setWindowTitle("WIFI LIST")
		#quality, ssid, user, pwd
		self.setColumnCount(3)

		self.verticalHeader().hide()
		self.setHorizontalHeaderLabels(['quality', 'wifi', 'password'])
		self.setShowGrid(False)
		# table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

		#[[quality, name, pwd]]
		# self.item(0, 2).setFlags(self.item(0, 2).flags() ^ QtCore.Qt.ItemIsEditable)

		self.pw.start(
			RunnableFunc(
				self.asynFillTable
				)
			)
		self.wifiQuerySignal.connect(self.asynFillTableCallBack)

	def asynFillTable(self):
		wifiList = self.wifiManager.getWifiList()
		print(wifiList)
		self.wifiQuerySignal.emit(wifiList)
		#pull data and emit signal


	def asynFillTableCallBack(self, wifiList):
		for w in wifiList:
			self.appendStrRow(visulizeSignal(w))
		self.pw.start(
			RunnableFunc(
				wifiManager().connect_saved
				)
			)

	def appendStrRow(self, data):
		x = self.rowCount()
		self.insertRow(x)
		for i, v in enumerate(data) :
			item = QtGui.QTableWidgetItem(v)
			item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
			
			item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
			self.setItem(x, i, item)
			

if __name__ == '__main__':
	try:
		visulizeSignal(['59/70'])
		# app = QtGui.QApplication(sys.argv)
		# wrapper = QtGui.QMainWindow()
		# wrapper.setCentralWidget(WifiTableView())
		# wrapper.setGeometry(400, 400, 800, 480)
		# wrapper.show()
		# sys.exit(app.exec_())
	except Exception as e:
		print(e)


		