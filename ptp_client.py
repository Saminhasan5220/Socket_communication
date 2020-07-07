import sys
import time
import socket
import threading
class Server:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	def __init__(self,ip='127.0.0.1',port=5001):
		self.ip = ip
		self.port = port
		self.running = True

	def run(self):
		print("Client UP and running ...")
		self.recieve_thread = threading.Thread(target=self.recieve)
		self.recieve_thread.daemon = True
		self.recieve_thread.start()
		while self.running:
			pass
		counter = 0
		while self.recieve_thread.is_alive() or self.sending_thread.is_alive():
			print("Recive thread is alive:",self.recieve_thread.is_alive(), "Sending thread is alive:",self.sending_thread.is_alive(),"Counter:",counter,end="\r")
			counter +=1
		self.quit()
		
	def recieve(self):
		self.sock.connect((self.ip,self.port))	
		self.sending_thread = threading.Thread(target=self.send)
		self.sending_thread.daemon = True
		self.sending_thread.start()
		while self.running:
			try:
				if self.running and self.sock:
					data = self.sock.recv(1024)

				if not data:
					print("not data")
					break
				data = data.decode("utf-8")
				print("From Server to Client =>",data)
			except ConnectionResetError or ConnectionAbortedError:
				print("Server Disconnected")
				self.running =False
				break

	def send(self):
			while self.running:
				x = time.time()#input("Type to send message:")

				time.sleep(1)
				if self.sock:
					try:	
						msg	 = str(x)
						self.sock.send(msg.encode('utf-8'))
						print("From Client to Server->",msg)
					except OSError:
						break
				else:
					break
			
			
	def quit(self):
		self.running = False
		if self.sock:
			self.sock.close()
		sys.exit()
		
		
		
server = Server()
try:
	server.run()
except KeyboardInterrupt:
	pass
