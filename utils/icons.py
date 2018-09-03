from PyQt4 import QtGui

icon_dict={
    'add_record':'icons/new_record.png',
    'back':'icons/back_48.png',
}

def get_icon(name):
    label = QtGui.QLabel()
    label.setPixmap(QtGui.QPixmap(icon_dict[name]))
    return label