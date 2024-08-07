import socket
import threading

def protocol_header(usernamelen, data_length):
    return usernamelen.to_bytes(1, "big") + data_length.to_bytes(4, "big")


def send_message(sock, server_address, server_port, name):
    while True:
        sendmessage = input("")
        print("\033[1A\033[1A") 
        print("You: " + sendmessage)
        name_bits = name.encode('utf-8')
        message_bits = sendmessage.encode('utf-8')
        header = protocol_header(len(name_bits), len(message_bits))
        data = name_bits + message_bits

        sock.sendto(header, (server_address, server_port))
        sock.sendto(data, (server_address, server_port))


def receive_message(sock):
    try:
        while True:
            receive = sock.recvfrom(1024)[0].decode('utf-8')
            if receive == 'close':
                print('close')
                sock.close()
                break
            print(receive)


    except Exception as e:
        print("Error in receive_message:", e)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




server_port = 9001
address = ''
port = 9051

sock.bind((address,port))

name = input("My name is: ")


send_thread = threading.Thread(target=send_message, args=(sock, address, server_port, name))
receive_thread = threading.Thread(target=receive_message, args=(sock,))


send_thread.start()
receive_thread.start()

send_thread.join()
receive_thread.join()