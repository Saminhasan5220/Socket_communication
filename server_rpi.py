import sys
import time
import socket
import threading
import RPi.GPIO as GPIO
from microcontroller import Arduino
class Server:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    def __init__(self,ip='192.168.1.5',port=10000):
        self.ip = ip
        self.port = port
        self.sock.bind((self.ip,self.port))
        self.sock.listen(1)
        self.running = True
        self.client = None
        self.client_address = None
        GPIO.setmode(GPIO.BOARD)
        # Set pins 11 & 12 as outputs, and define as PWM servo1 & servo2
        GPIO.setup(11,GPIO.OUT)
        self.servo1 = GPIO.PWM(11,50) # pin 11 for servo1
        GPIO.setup(12,GPIO.OUT)
        self.servo2 = GPIO.PWM(12,50) # pin 12 for servo2
        # Start PWM running on both servos, value of 0 (pulse off)
        self.servo1.start(0)
        self.servo2.start(0)

    def scale(self, x,  in_min,  in_max,  out_min,  out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    def run(self):
        print("Server UP and running ...")
        self.recieve_thread = threading.Thread(target=self.recieve)
        self.recieve_thread.daemon = True
        self.recieve_thread.start()
        #self.send_video()
        while self.running:
            pass
        counter = 0
        while self.recieve_thread.is_alive() or self.sending_thread.is_alive():
            print("Recive thread is alive:",self.recieve_thread.is_alive(), "       Sending thread is alive:",self.sending_thread.is_alive(),"Counter:",counter,end="\r")
            counter +=1
        self.quit()
    def recieve(self):      

        self.client,self.client_address = self.sock.accept()
        self.sending_thread = threading.Thread(target=self.send)
        self.sending_thread.daemon = True
        self.sending_thread.start()

        while self.running:
            try:
                if self.running and self.client:
            
                    data = self.client.recv(1024)

                if not data:
                    print("not data")
                    break
                    
                data = data.decode("utf-8")
                #print("Client address:", str(self.client_address[0]),':',str(self.client_address[1]))
                #print("From Client to server=>",data,type(data),len(data))
                self.control(data)
            except ConnectionResetError or ConnectionAbortedError:
                self.running =False
                print("Client Disconnected")
                break

    def send(self):
        #time.sleep(20)
        self.board = Arduino()
        connection = self.board.connect()
        while self.running and connection:
                
            #x = time.time()#input("Type to send message:")
            x = self.board.send(0)
            time.sleep(0.05)
            if not x:
                print("No IMU")
                x = str(([0, 0, 0]))
                
            if self.client:
                try:    
                    msg  = str(x[0]) + ',' +str(x[1]) + ',' +str(x[2])
                    self.client.send(msg.encode('utf-8'))
                    #print("From Server to Client->",msg)
                except OSError:
                    break
            else:
                break
        self.board.disconnect()
    def control(self,command):
        command = tuple(command.split(','))
        #print(command[0],command[1],end="\r")
        try:
            t = float(command[0])
            s = float(command[1])
        except ValueError:
            t = 0.0
            s = 0.0
        throttle = self.scale(float(t),-1.0,1.0,4.0,8.0)
        steering = self.scale(float(s),-1.0,1.0,4.0,8.0)
        print(throttle,steering,end="\r")
        self.servo1.ChangeDutyCycle(throttle)
        self.servo2.ChangeDutyCycle(steering)
        time.sleep(0.3)
        self.servo2.ChangeDutyCycle(0)
        self.servo1.ChangeDutyCycle(0)
    def quit(self):
        self.running = False
        if self.client:
            self.client.close()
        self.servo1.stop()
        self.servo2.stop()
        GPIO.cleanup()
        sys.exit()

        
server = Server()
try:
    server.run()
except KeyboardInterrupt:
    pass
