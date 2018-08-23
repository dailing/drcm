from time import gmtime, strftime
class PatientInfo():
	"""docstring for BasicInfo"""
	def __init__(self, name, pid, gender, birthday, leftEye):
		# PatientInfo('name', '1234', False, '2018-09-08', True)
		self.name = name
		self.pid = pid
		self.gender = gender
		self.birthday = birthday
		self.leftEye = leftEye
		self.timeOnCreation = strftime("%Y-%m-%d", gmtime())

	def getCreationTime(self):
		return self.timeOnCreation
		
	def isMale(self):
		return self.gender

	def getName(self):
		return self.name

	def getPid(self):
		return self.pid

	def isLeftEye(self):
		return self.leftEye

	def getBirthday(self):
		return self.birthday

class ImageInfo(PatientInfo):
	# ImageInfo('name', 'pid', 'gender', 'birthday', 'left', 'ts', 'uuid', 'data')
	def __init__(self, name, pid, gender, birthday, leftEye):
		PatientInfo.__init__(self, name, pid, gender, birthday, leftEye)
		pass
		# self.timestamp = timestamp
		# self.uuid = uuid
		# self.data = data
		
	@staticmethod
	def fromPatientInfo(patient):
		instance = ImageInfo(
			patient.getName(), 
			patient.getPid(), 
			patient.isMale(),
			patient.getBirthday(),
			patient.isLeftEye()
			)
		return instance

	def setTime(self, timestamp):
		self.timestamp = timestamp
		return self

	def setUUID(self, uuid):
		self.uuid = uuid

	def setData(self, data):
		self.data = data

	def getData(self):
		return self.data

	def getUUID(self):
		return self.uuid

	def getTimeId(self):
		return self.timestamp


def main():
	imageInfo = ImageInfo('name', 'pid', 'gender', 'birthday', 'left', 'ts', 'uuid', 'data')
	print(imageInfo.getName())
if __name__ == '__main__':
	main()