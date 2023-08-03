import socket 
from PIL import Image
import os

HOST = 'localhost'
PORT = 5000
origin = (HOST, PORT)
dest = (HOST, 3000)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(origin)


#------------RECEBIMENTO DO ARQUIVO -----------------------------------

print("Server is ready!")
file_bytes = b""

file_name, clientAddress = serverSocket.recvfrom(1024) 
file_name = file_name.decode()
file_name = "received_"+file_name
file = open(file_name, "wb")

dcount = 0
while True:
  datagram, clientAddress = serverSocket.recvfrom(1024)
  dcount += 1
  print(f"datagram {dcount} recebido do cliente ({clientAddress})")

  if(datagram == b"<END>"):
    dcount = 0
    break
  else:
    file_bytes += datagram
print("envio finalizado.")

file.write(file_bytes)
file.close()

#------DEVOLUCAO DO ARQUIVO----------------------------------------------------------
file = open(file_name, "rb")
serverSocket.sendto(file_name.encode(), dest) #Envia nome do arquivo
while True:
    file_data = file.read(1024)
    if not file_data :
        serverSocket.sendto(b"<END>", dest) 
        break
    serverSocket.sendto(file_data, dest)

file.close()
serverSocket.close()
