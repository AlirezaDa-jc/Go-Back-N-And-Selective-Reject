# سرور (گیرنده)
import socket

refused_packets = []
received_data = []


def receiver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print('Server is listening...')
    conn, addr = server_socket.accept()
    print(f'Connected by {addr}')
    Rn = 0
    while True:
        packet = int(conn.recv(1024).decode('utf-8'))
        if packet == Rn:
            accept_packet(packet)
            received_data.append(packet)
        elif packet != Rn and packet not in refused_packets:
            for i in range(Rn, packet):
                refused_packets.append(Rn)
                received_data.append(None)
            Rn = packet
            accept_packet(packet)
            received_data.append(packet)
        elif packet in refused_packets:
            refused_packets.remove(packet)
            received_data.insert(packet, packet)
            accept_packet(packet)
            received_data.append(packet)
        Rn += 1

        if len(refused_packets) > 0:
            conn.sendall(str(f'Nack-{refused_packets[0]}').encode('utf-8'))


def accept_packet(packet):
    print(f'Accepted packet: {packet}')


def refuse_packet(packet):
    print(f'Refused packet {packet} because it is not the expected number.')
    refused_packets.append(packet)


receiver()
