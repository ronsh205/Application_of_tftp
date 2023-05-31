import socket
import time
import os  # import system

localIP = "127.0.0.1"

# localPort = 2001
localPort = 69

bufferSize = 512
buffername = 60
msgFromServer = "Hello UDP Client"

bytesToSend = b'0004'

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

# UDPServerSocket.bind((arg, localPort))
UDPServerSocket.bind(("",localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while True:
    # bytesAddressname = UDPServerSocket.recvfrom(buffername)  # add send name file
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    # name_f = bytesAddressname[0]
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    print(message.decode())
    # print("[ {} ]".format(name_f))# data from client
    if message == b'0001':
        print("read request")
        UDPServerSocket.sendto(bytesToSend, address)
        print("send ack to client")
        mag_rev = message.decode()
        print(mag_rev)
        rev_name = UDPServerSocket.recvfrom(buffername)
        # input_directory = "file_server"  # define location of files want  work
        # files = os.listdir(input_directory)  # open location work
        #
        # print("list files have in directory ")
        # for idx, file in enumerate(files):  # see option files have in dictionaries
        #     print("[", idx, "] ", file)
        # file_dir_number = int(input("input files :"))  # choice one option from the list
        #
        # name_file_work = files[file_dir_number]  # name of file chose
        # print(name_file_work)
        # data_rcv = []
        count = 0
        file_from_server = rev_name[0].decode()
        print(file_from_server)

        while True:
            file_St = open("file_server/" + file_from_server, "rb")
            data_rcv = file_St.read(511)
            print(data_rcv)
            UDPServerSocket.sendto(data_rcv, address)

            count += 512
            time.sleep(2)
            data_rcv = file_St.seek(count)

            if data_rcv:
                break

    if message == b'0002':
        print("write request")
        mag_rev = message.decode()
        print(mag_rev)
        print(type(mag_rev))
        UDPServerSocket.sendto(bytesToSend, address)
        bytesAddressname = UDPServerSocket.recvfrom(buffername)  # add send name file
        name_f = bytesAddressname[0]
        print(name_f.decode())
        byte_list = []
        f = open("file_client/" + name_f.decode(), "r")
        while True:
            byte = f.read(512)
            with open('file_server/' + name_f.decode(), 'a+') as filehandle:
                filehandle.writelines(byte)
                print("count byte receive from client and write to server : {} ".format(len(byte)))
                time.sleep(1.5)
            if not byte:
                break

            # print(byte)

        f.close()
    clientMsg = "Message from Client:{}".format(message)  # data from client
    # clientIP = "Client IP Address:{}".format(address)

    UDPServerSocket.sendto(bytesToSend, address)
