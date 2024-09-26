# کلاینت
import socket
import threading
import time

not_sent_packets = set()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

def send_packets():
    data = list(range(17))  # داده‌ها از 0 تا 16
    for Sb in range(len(data)):
        if Sb == 6:
            continue
        time.sleep(2)
        client_socket.sendall(str(data[Sb]).encode('utf-8'))
    while len(not_sent_packets) > 0:
        client_socket.sendall(str(data[not_sent_packets.pop()]).encode('utf-8'))


def receive_packets():
    while True:
        data = client_socket.recv(1024)
        print(data.decode())
        if "Nack" in data.decode():
            not_sent_packets.add(int(data.decode().split('-')[1]))


def client():

    threading.Thread(target=send_packets).start()
    threading.Thread(target=receive_packets).start()  # client_socket.close()


if __name__ == "__main__":
    client()
