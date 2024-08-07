import socket
import time
import threading

def remove_client(user_info, usertime):
    while True:
        current_time = time.time()
        remove_user_list = []
        for address, t in usertime.items():
            if current_time - t >= 10:
                if address in user_info:
                    remove_user_list.append(address)

        
        for address in remove_user_list:
            sock.sendto("close".encode('utf-8'), address)
            del user_info[address]
            del usertime[address] 
            print('close')




def sendreceive(sock, user_info, usertime):
    while True:
        print('waiting to receive message')
        header, address = sock.recvfrom(8)
        print(f'address: {address}')


        name_length = int.from_bytes(header[:1], "big")
        message_length = int.from_bytes(header[1:], "big")

        data, address = sock.recvfrom(1024)

        username_bits = data[:name_length]
        message_bits = data[name_length: name_length+message_length]




        username = username_bits.decode('utf-8')
        #addressとnameを結びつける
        user_info[address] = username
        
        usertime[address] = time.time()

        message = message_bits.decode('utf-8')
        print(f"name: {username}, data: {data.decode('utf-8')}, message: {message}")

        for key in user_info:
            if key == address: continue
            sock.sendto((f"{username}: {message}").encode('utf-8'), key)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001
print('starting up on port {}'.format(server_port))

sock.bind((server_address, server_port))
user_info = {} #user_info[address] = username
usertime = {} #usertime[address] = time.time()

send_thread = threading.Thread(target=sendreceive, args=(sock, user_info, usertime))
remove_thread = threading.Thread(target=remove_client, args=(user_info, usertime))

send_thread.start()
remove_thread.start()

send_thread.join()
remove_thread.join()
