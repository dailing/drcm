class PatientInfo():
	def __init__(self, name, pid, gender, birthday, address, timestamp, uuid):
		
		self.name = name
		self.pid = pid
		self.gender = gender
		self.birthday = birthday
		self.address = address
		self.timestamp = timestamp
		self.uuid = uuid
		

	def setTime(self, timestamp):
		self.timestamp = timestamp
		return self

	def setUUID(self, uuid):
		self.uuid = uuid

	def getName():
		return self.name