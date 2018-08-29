"""models for patient and fundus images storage"""
from peewee import SqliteDatabase, Model, TextField, DateTimeField, CharField, ForeignKeyField, BlobField
import datetime
import cv2
import numpy as np
import utils.logFormatter
import uuid

database = SqliteDatabase('db.db')

logger = utils.logFormatter.setupLogger('model')


class BaseModel(Model):
    class Meta:
        database = database


class Patient(BaseModel):
    name = TextField()
    pid = CharField(unique=True, primary_key=True)
    created = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return '{}, id={}'.format(self.name, self.pid)

    def get_images(self):
        return FundusImage \
            .select() \
            .where(FundusImage.pid == self.pid) \
            .order_by(FundusImage.created)

    def add_image(self, image):
        image_record = FundusImage(pid=self.pid)
        image_record.read_img(image)
        image_record.save()


class FundusImage(BaseModel):
    pid = ForeignKeyField(Patient, field='pid')
    uuid = TextField(unique=True, default=lambda: str(uuid.uuid4()), primary_key=True)
    payload = BlobField(null=False)
    created = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return 'pid:[{}], created at:{}, size:{}'.format(
            self.pid,
            self.created,
            len(self.payload)
        )

    def read_img(self, image):
        """
        read image from numpy array or a file and save it into payload.
        :param image: path of the image or nd_array of the image
        :return: bool, True for success
        """
        # get file from disk here
        if type(image) is str:
            image = cv2.imread(image, cv2.IMREAD_COLOR)

        if type(image) is np.ndarray:
            succ, binary_payload = cv2.imencode('.png', image)
            binary_payload = binary_payload.tobytes()
            # logger.info(binary_payload)
            self.payload = binary_payload
            return True
        else:
            logger.error('input type not recognized:{}'.format(type(image)))
        return False

    def get_img(self):
        """
        get and decode image from db
        :return: nd_array
        """
        if self.payload is None:
            return None
        try:
            payload = np.frombuffer(self.payload, dtype=np.uint8)
            return cv2.imdecode(payload, cv2.IMREAD_COLOR)
        except Exception as e:
            logger.error(e)
            return None

    def show(self):
        img = cv2.resize(self.get_img(), (900, 500))
        cv2.imshow('image show', img)
        cv2.waitKey()
        cv2.destroyAllWindows()


database.connect()
database.create_tables([Patient, FundusImage])


class Patients():
    def __init__(self):
        pass

    def __getitem__(self, item):
        """
        the index function
        :param item:
            if item is int, return the corresponding patient. ordered by time ASC,
                So you can use p[0] to get the earliest created item.
            if a string is given, it is assumed as the PID of patient.
                So p['asd'] will return the patient with id 'asd'
            if a slice is given, returns the corresponding records, this make the
                paging easy
            if a tuple is given the first item should be the page number, second
                is items per page. So p[2,10] returns the item in page 2, 10 items
                in page.

        :return:
        """
        if type(item) is int:
            if item > self.__len__():
                raise IndexError('{} out of index'.format(item))
            return list(Patient.select().order_by(Patient.created.desc()).offset(item).limit(0))[0]
        elif type(item) is str:
            return Patient.get(Patient.pid == item)
        elif type(item) is slice:
            start, end = item.start, item.stop
            if not ((item.step is None) or (item.step == 1)):
                logger.error('Step must be 1, not {}'.format(item.step))
                return None
            if start is None:
                start = 0
            if end is None:
                end = self.__len__()
            elif end > self.__len__():
                raise IndexError('{} out of index'.format(end))
            return list(Patient.select().order_by(Patient.created.desc()).offset(start).limit(end - start))
        elif type(item) is tuple and len(item) == 2:
            page, item_per_page = item
            start,end = page * item_per_page, page * item_per_page + item_per_page
            end = min(end,self.__len__())
            if end <=start:
                return []
            return self[start:end]
        else:
            logger.error('Index Error: type:{}, value:{}'.format(type(item), item))

    def __len__(self):
        return Patient.select().count()

    def add_patient(self, name, pid=None):
        """
        add patient to database
        :param name: name of patient
        :param pid: id of patient
        :return: pid if successful, None if error
        """
        if pid is None:
            pid = str(uuid.uuid4())
        p = Patient(name=name, pid=pid)
        try:
            p.save()
            return p.pid
        except Exception as e:
            logger.error(e)
        return None


if __name__ == '__main__':
    p = Patients()
    pid = p.add_patient('Bob', '123')
    pid = p.add_patient('test_pathent1', '1234')
    pid = p.add_patient('test_pathent2', '1235')
    logger.info(len(p))
    logger.info(p[0])
    logger.info(p['123'])
    logger.info(p[:3])
    logger.info(p[1, 2])
    logger.info(p[0, 2])

    bob = p['123']
    bob.add_image('/home/d/workspace/drsys/classification_service/app/yanhua_test/25422_right.jpeg')
    imgs = (bob.get_images())
    logger.info(len(imgs))
    logger.info(imgs[0])
    imgs[0].show()
