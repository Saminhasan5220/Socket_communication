from serial import*
class Arduino:
	def __init__(self,port="/dev/ttyUSB0",baudrate=115200):
		self.port = port
		self.baudrate = baudrate
		self.msg = "IMU ready"
		self.connected = False
		self.board = None
		
	def connect(self):
		try:
			msg =""
			self.board = Serial(self.port,self.baudrate)
			while msg.find(self.msg) == -1:
				while self.board.inWaiting() == 0:
					pass
				msg = self.board.readline().decode('utf-8')
			
			self.connected =True
			self.board.flush()
			return self.connected 
		except Exception as e:
			print(e)
			return self.connected 
			
	def send(self,d):
		if type(d) != str:
			d =str(d)
		msg = d + '\n'
		msg = msg.encode('utf-8')
		self.board.write(msg)
		while(self.board.inWaiting()==0):
			pass
		data = self.board.readline().decode('utf-8').split(',')
		data[len(data) - 1] = data[len(data) - 1].rstrip()
		return data

	def disconnect(self):
		self.board.close()
		self.connected = False
		
"""		
import time

Mega = Arduino()
connection = Mega.connect()
while connection:

	try:
		print(Mega.send(0))
		
	except KeyboardInterrupt:
		Mega.disconnect()
		break
		
print("Done")
"""
