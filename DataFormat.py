class DataFormat():
	def __init__(self, name, pid, birthday, address, timestamp, utc):
		
		self.name = name
		self.pid = pid
		self.birthday = birthday
		self.address = address
		self.timestamp = timestamp
		self.utc = utc
		

	def setTime(self, timestamp):
		self.timestamp = timestamp
		return self

	def setutc(self, utc):
		self.utc = utc