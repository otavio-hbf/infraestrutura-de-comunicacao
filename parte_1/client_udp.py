import socket
import os

HOST = 'localhost'
PORT = 5000
dest = (HOST, PORT)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.bind(('localhost', 3000))


#-------------ENVIO DO ARQUIVO -------------------------------------

file_src = "pikachuzera.png"
file = open(file_src, "rb")
file_size = os.path.getsize(file_src)
print(f"O tamanho do arquivo é : {file_size} bits")

clientSocket.sendto(file_src.encode(), dest) #Envia nome do arquivo

while True:
    file_data = file.read(1024)
    if not file_data :
        clientSocket.sendto(b"<END>", dest) 
        break
    clientSocket.sendto(file_data, dest)

#---------- RECEBENDO O ARQUIVO DE VOLTA ---------------------------

file_bytes = b""

file_name, clientAddress = clientSocket.recvfrom(1024) 
file_name = file_name.decode()
file_name = "client_"+file_name
file = open(file_name, "wb")

dcount = 0
while True:
  datagram, serverAddress = clientSocket.recvfrom(1024)
  dcount += 1
  print(f"datagram {dcount} recebido do servidor ({clientAddress})")

  if(datagram == b"<END>"):
    dcount = 0
    break
  else:
    file_bytes += datagram
print("devolucao finalizada.")

file.write(file_bytes)
file.close()
clientSocket.close()
