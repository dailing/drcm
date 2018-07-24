class PatientInfo():
	def __init__(self, name, pid, gender, birthday, leftEye, timestamp, uuid, data):
		
		self.name = name
		self.pid = pid
		self.gender = gender
		self.birthday = birthday
		self.leftEye = leftEye
		self.timestamp = timestamp
		self.uuid = uuid
		self.data = data
		

	def setTime(self, timestamp):
		self.timestamp = timestamp
		return self

	def setUUID(self, uuid):
		self.uuid = uuid

	def setData(self, data):
		self.data = data

	def isMale(self):
		return self.gender

	def getName(self):
		return self.name

	def getPid(self):
		return self.pid

	def isLeftEye(self):
		return self.leftEye

	def getData(self):
		return self.data

	def getUUID(self):
		return self.uuid

	def getBirthday(self):
		return self.birthday

	def getTimeId(self):
		return self.timestamp