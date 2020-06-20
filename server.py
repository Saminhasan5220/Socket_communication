import sys
import time
import socket
import threading

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
		try:
			print("Server started")
			while self.running:
				c,a = self.sock.accept()
				cThread = threading.Thread(target=self.handler,args=(c,a))
				cThread.daemon = True
				cThread.start()

				self.connections.append(c)
				print(str(a[0]),':',str(a[1]),"connected")
		except KeyboardInterrupt:
			self.running = False
			print("Server closing")
			for connection in self.connections:
				connection.close()
			self.sock.close()

			sys.exit()

				
	def handler(self,c,a):
		cTick = threading.Thread(target=self.tick,args=(c,a))
		cTick.daemon = True
		cTick.start()
		while self.running:
			data = c.recv(1024)
			if not data:
				print(str(a[0]),':',str(a[1]),"disconnected")
				c.close()
				break
			data = data.decode("utf-8")
			print("From", str(a[0]),':',str(a[1]),"to server:",data)
	def tick(self,c,a):
		while True:
			try:
				msg  = str(time.time())
				c.send(msg.encode('utf-8'))
				time.sleep(1)
			except:

				break


server = Server()
server.run()
