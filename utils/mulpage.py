import sys
from PyQt4 import QtGui, QtCore

#http://stackoverflow.com/questions/36675609/how-can-i-create-multi-page-applications-in-pyqt4/36676917

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        widget1 = QtGui.QLabel("Page 1")
        widget2 = QtGui.QLabel("Page 2")

        btn1 = QtGui.QPushButton("Page 1")
        btn1.setCheckable(True)
        btn1.setChecked(True)
        btn1.toggled.connect(widget1.setShown)
        btn2 = QtGui.QPushButton("Page 2")
        btn2.setCheckable(True)
        btn2.setChecked(True)
        btn2.toggled.connect(widget2.setShown)

        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(widget1)
        vlayout.addWidget(widget2)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(btn1)
        hlayout.addWidget(btn2)
        vlayout.addLayout(hlayout)

        widget = QtGui.QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())