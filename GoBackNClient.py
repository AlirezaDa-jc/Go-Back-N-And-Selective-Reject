# کلاینت
import socket
import threading
import time

received_ack = []

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

def send_packets():
    window_from = 0
    Sb = 0
    Sm = 5  # اندازه پنجره
    data = list(range(17))  # داده‌ها از 0 تا 16
    send_all = True
    while True:
        time.sleep(1)
        if send_all:
            for Sb in range(window_from, min(Sb + Sm, len(data))):
                time.sleep(1)
                client_socket.sendall(str(data[Sb]).encode('utf-8'))
            Sb = Sb + 1
            send_all = False
        elif window_from in received_ack:
            window_from += 1
            if Sb < len(data):
                client_socket.sendall(str(data[Sb]).encode('utf-8'))
                Sb += 1
            else:
                break
        else:
            Sb = window_from
            send_all = True


def receive_packets():
    while True:
        data = client_socket.recv(1024)
        print(data.decode())
        if "Ack" in data.decode():
            received_ack.append(int(data.decode().split('-')[1]))


def client():

    threading.Thread(target=send_packets).start()
    threading.Thread(target=receive_packets).start()  # client_socket.close()


if __name__ == "__main__":
    client()
