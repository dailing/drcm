class PatientInfo():
	def __init__(self, name, pid, gender, birthday, address, timestamp, utc):
		
		self.name = name
		self.pid = pid
		self.gender = gender
		self.birthday = birthday
		self.address = address
		self.timestamp = timestamp
		self.utc = utc
		

	def setTime(self, timestamp):
		self.timestamp = timestamp
		return self

	def setUtc(self, utc):
		self.utc = utc

	def getName():
		return self.name