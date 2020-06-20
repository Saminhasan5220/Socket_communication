import sys
import time
import socket
import threading


class Client:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	def __init__(self,ip='127.0.0.1',port=5001):
		self.ip = ip
		self.port = port
		self.connect()
		print("connected")
		self.running = True
		iThread = threading.Thread(target=self.sendData)
		iThread.daemon = True
		iThread.start()

		
		while self.running:

			try:
				data = self.sock.recv(1024)
				if not data:

					print("Server quit")
					self.running = False
					self.sock.close()
					break
				print("Recieved:",data.decode('utf-8'))
			except KeyboardInterrupt:
				self.running = False
				address = self.sock.getsockname()
				closing_msg = "leaving"
				self.sock.send(closing_msg.encode('utf-8'))
				print("Disconnecting")
				self.sock.close()
				break

		while iThread.is_alive():

			print("Waiting for thread to close",end="\r")
		sys.exit()
	def connect(self):
		try:
			self.sock.connect((self.ip,self.port))	
		except ConnectionRefusedError:
			print("server not running")
			print("Trying to reconncet in 1 seconds")
			time.sleep(1)
			self.connect()
			
	def sendData(self):
		while self.running:
			try:
				msg  = str(time.time())
				self.sock.send(msg.encode('utf-8'))
				time.sleep(1)
			except ConnectionResetError:
				self.running = False
				break

			



client = Client()
				
