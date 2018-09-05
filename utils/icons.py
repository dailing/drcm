from PyQt4 import QtGui

icon_dict={
    'add_record':'icons/new_record.png',
    'back':'icons/back_48.png',
    'forward':'icons/forward_48.png',
    'open_camera':'icons/camera_48.png',
    'save_record':'icons/save_48.png',
    'wifi_config' : 'icons/wifi_48.png',
    'refresh': 'icons/refresh_48.png'
}

def get_icon(name):
    label = QtGui.QLabel()
    label.setPixmap(QtGui.QPixmap(icon_dict[name]))
    return label