from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import QWidget, QApplication
import sys
from logs import get_logger
import time
import random
import logging

logger = get_logger('conn_log', logging.DEBUG)

class Uploader(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def send_pic(self, pic_info):
        logger.debug('send pic')
        time.sleep(1)
        self.emit(SIGNAL("pic_upload_finished(bool)"),
                  random.random() > 0.5)
        return True

    def run(self):
        logger.debug('thread running')
        time.sleep(1)
        self.send_pic(None)


if __name__ == '__main__':
    logger.debug('test start')
    class Window(QWidget):

        def __init__(self, parent=None):
            QWidget.__init__(self, parent)

            self.thread = Uploader()
            self.thread.start()
            self.connect(self.thread, SIGNAL("pic_upload_finished(bool)"), self.test)
            self.setWindowTitle(self.tr("testing"))

        def test(self, succ: bool):
            logger.debug('succ')

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())