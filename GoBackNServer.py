# سرور (گیرنده)
import socket


def receiver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print('Server is listening...')
    conn, addr = server_socket.accept()
    print(f'Connected by {addr}')
    Rn = 0
    first = True
    while True:
        packet = int(conn.recv(1024).decode('utf-8'))
        if packet == Rn:
            if packet == 6 and first:
                first = False
                continue
            accept_packet(packet)
            conn.sendall(str(f'Ack-{Rn}').encode('utf-8'))
            Rn += 1
        else:
            refuse_packet(packet)


def accept_packet(packet):
    print(f'Accepted packet: {packet}')


def refuse_packet(packet):
    print(f'Refused packet {packet} because it is not the expected number.')


receiver()
