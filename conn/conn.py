from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import QWidget, QApplication
import sys
import time
import random
import logging
import cv2
import logging
import sys
import datetime
import os.path


def get_logger(name, print_level=logging.DEBUG):
    formater = logging.Formatter(
        fmt="%(levelname)6s %(name)s[%(filename)s.%(lineno)-3d %(asctime)s] %(message)s",
        datefmt='%H:%M:%S',
    )
    time_now = datetime.datetime.now().strftime("%Y_%m_%d.%H_%M_%S")
    logger = logging.getLogger(name)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formater)
    stream_handler.setLevel(print_level)
    try:
        os.mkdir('log')
    except Exception as e:
        pass
    file_handler = logging.FileHandler('log/{}.{}.log'.format(time_now, name))
    file_handler.setFormatter(formater)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger


logger = get_logger('conn_log', logging.DEBUG)


class Uploader(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.db = pymongo.MongoClient(
            'mongo_db',
            27017,
            username='root',
            password='example').fundus_images

    def _save_file(self, pid, arr, uuid):
        cv2.imencode('png', arr)
        # gfs = gridfs.GridFS(self.db)
            # gfs.put(
            #     open(f, 'rb').read(),
            #     pid=pid,
            #     uuid = uuid,
            # )

    def send_pic(self, pic_info):
        logger.debug('send pic')
        time.sleep(1)
        self.emit(SIGNAL("pic_upload_finished(bool)"),
                  random.random() > 0.5)
        return True

    def run(self):
        logger.debug('thread running')
        time.sleep(1)
        self.send_pic(True)


if __name__ == '__main__':
    logger.debug('test start')

    class Window(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent)

            self.thread = Uploader()
            self.thread.start()
            self.connect(self.thread, SIGNAL("pic_upload_finished(bool)"), self.test)
            self.setWindowTitle(self.tr("testing"))

        def test(self, succ):
            logger.debug('succ')
            logger.debug(succ)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())