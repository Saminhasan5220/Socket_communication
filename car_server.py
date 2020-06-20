import sys
import time
import socket
import threading
from microcontroller import Arduino
class Server:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	connections = []
	def __init__(self,ip='0.0.0.0',port=5001):
		self.ip = ip
		self.port = port
		self.sock.bind((self.ip,self.port))
		self.sock.listen(1)
		self.running = True
		
	def run(self):

		print("Server started")

		c,a = self.sock.accept()
		cTick = threading.Thread(target=self.tick,args=(c,a))
		cTick.daemon = True
		cTick.start()
		#cThread = threading.Thread(target=self.handler,args=(c,a))
		#cThread.daemon = True
		#cThread.start()
		self.connections.append(c)
		print(str(a[0]),':',str(a[1]),"connected")
		while self.running:
			try:
				self.handler(c,a)
			except KeyboardInterrupt:
				self.quit()

						
	def handler(self,c,a):

		while self.running:
			data = c.recv(1024)
			if not data:
				print(str(a[0]),':',str(a[1]),"disconnected")
				c.close()
			data = data.decode("utf-8")
			print("From", str(a[0]),':',str(a[1]),"to server:",data,end="\r")
	def tick(self,c,a):
		Mega = Arduino()
		connection = Mega.connect()
		while connection and self.running:
			try:	
				x = Mega.send(0)
				msg  = str(x)
				c.send(msg.encode('utf-8'))
			except KeyboardInterrupt:
				Mega.disconnect()
				break
				
				
	def quit(self):
		self.running = False
		print("Server closing")
		for connection in self.connections:
			connection.close()
		#self.sock.close()
		#sys.exit()
		"""
		while True:
			try:
				msg  = str(time.time())
				c.send(msg.encode('utf-8'))
				time.sleep(1)
			except:

				break
		"""


server = Server()
server.run()
