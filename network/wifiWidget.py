import sys
import logging

from PyQt4 import QtGui, QtCore




class WifiTableView(QtGui.QTableWidget):
	"""wifi mananger table list view"""
	def __init__(self):
		QtGui.QTableWidget.__init__(self)
		self.initTable()
		
	def tabCellClicked(self, i, j):
		if j != 1:
			return
		print(i,j)
		print(str(self.item(i, 2).text()))

	def initTable(self):
		# table.itemClicked.connect(self.tabItemDoubleClicked)
		self.cellClicked.connect(self.tabCellClicked)
		tableItem 	= QtGui.QTableWidgetItem()
		self.setWindowTitle("WIFI LIST")
		#quality, ssid, user, pwd
		self.setColumnCount(4)

		self.verticalHeader().hide()
		self.horizontalHeader().hide()
		self.setShowGrid(False)
		# table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

		#[[quality, name, pwd]]
		self.appendStrRow(['x', 'y', 'z'])
		

	@staticmethod
	def tabItemDoubleClicked(item):
		if item.column() != 1:
			return
		print(item, item.column())

	def appendStrRow(self, data):
		x = self.rowCount()
		self.insertRow(x)
		for i, v in enumerate(data) :
			item = QtGui.QTableWidgetItem(v)
			item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
			if i < 2 :
				item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
			self.setItem(x, i, item)

if __name__ == '__main__':
	try:
		app = QtGui.QApplication(sys.argv)
		wrapper = QtGui.QMainWindow()
		wrapper.setCentralWidget(WifiTableView())
		wrapper.setGeometry(400, 400, 800, 480)
		wrapper.show()
		sys.exit(app.exec_())
	except Exception as e:
		print(e)


		