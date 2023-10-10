from threading import Thread
import socket

class ShootingUDPServer:
	def __init__(self, localIP = "127.0.0.1", localPort = 20001, bufferSize  = 1024, name = "ShootingUDPServer"):
		self.name = name
		self.bufferSize = bufferSize
		self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.socket.bind((localIP, localPort))
		self.stopped = False
		self.readyToSend = False

	def start(self):
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		print("UDP server up and listening")
		return self

	def update(self):
		while True:
			if self.stopped:
				return
			bytesAddressPair = self.socket.recvfrom(self.bufferSize)
			self.message = bytesAddressPair[0]
			self.address = bytesAddressPair[1]
			clientMsg = "Message from Client:{}".format(self.message)
			clientIP  = "Client IP Address:{}".format(self.address)
			self.readyToSend = True
			

	def send(self, msg = "Holi"):
		if(self.readyToSend):
			bytesToSend = str.encode(msg)
			self.socket.sendto(bytesToSend, (self.address[0],20002))
	
	def read(self):
		return 0

	def release(self):
		self.release
 
	def stop(self):
		self.stopped = True
