import socket
import os  # import system
import time
import sys

msgFromClient = "Hello UDP Server"
msgFromClient_read = b'0001'  # read request
msgFromClient_write = b'0002'  # write request
bytesToSend = b'0004'
arg = sys.argv[1]

serverAddressPort = (arg, 69)

bufferSize = 512
bufferSizeAck = 124
# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
r_w = int(input("enter 0 to write or 1 to read/n"))
if r_w == 0:  # write request
    UDPClientSocket.sendto(msgFromClient_write, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from ack Server  {}".format(msgFromServer[0])

    input_directory = "file_client"  # define location of files want  work
    files = os.listdir(input_directory)  # open location work

    print("list files have in directory ")
    for idx, file in enumerate(files):  # see option files have in dictionaries
        print("[", idx, "] ", file)
    file_dir_number = int(input("input files :"))  # choice one option from the list

    name_file_work = files[file_dir_number]  # name of file chose
    print(name_file_work)
    data_rcv = []
    count = 0
    while True:
        file_St = open("file_client/" + name_file_work, "rb")
        data_rcv = file_St.read(511)
        print(data_rcv)

        UDPClientSocket.sendto(name_file_work.encode(), serverAddressPort)
        UDPClientSocket.sendto(data_rcv, serverAddressPort)
        count += 512
        time.sleep(2)
        data_rcv = file_St.seek(count)

        if data_rcv:
            break

elif r_w == 1:  # read request
    UDPClientSocket.sendto(msgFromClient_read, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)
    if msgFromServer[0] == b'0004':
        input_directory = "file_server"  # define location of files want  work
        files = os.listdir(input_directory)  # open location work

        print("list files have in directory ")
        for idx, file in enumerate(files):  # see option files have in dictionaries
            print("[", idx, "] ", file)
        file_dir_number = int(input("input files :"))  # choice one option from the list
        print(file_dir_number)
        name_file_work = files[file_dir_number]  # name of file chose
        print(name_file_work)
        name_from_server = UDPClientSocket.sendto(name_file_work.encode(), serverAddressPort)

        data_rcv = []
        count = 0
        data_from_server = UDPClientSocket.recvfrom(bufferSize)
        name_f = data_from_server[0]
        print(name_f)
        byte_list = []
        f = open("file_server/" + name_file_work, "r")
        while True:
            byte = f.read(512)
            with open('file_client/' + name_file_work, 'a+') as filehandle:
                filehandle.writelines(byte)
                print("count byte receive from server and write to client : {} ".format(len(byte)))
                time.sleep(1.5)
            if not byte:
                break

            # print(byte)

        f.close()

    # UDPServerSocket.sendto(bytesToSend, serverAddressPort)
    UDPClientSocket.sendto(msgFromClient_read, serverAddressPort)
