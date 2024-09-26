# سرور
import socket
import time


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    print('Connected by', addr)
    last_packet = -1
    last_frame = 0
    last_window_size = 0
    while True:
        try:
            time.sleep(5)
            data = conn.recv(1024)
            if not data:
                break
            if '6' in data.decode():
                continue
            print(data.decode())
            if "Poll Packet" in data.decode():
                print(f"Request Packet {last_frame}-{last_packet + 1}".encode())  # به کلاینت یه Request Packet می فرستیم
                conn.sendall(f"Request Packet {last_frame}-{last_packet + 1}".encode())  # به کلاینت یه Request Packet می فرستیم
                continue
            frame, packet, window_size = map(int, data.decode().split('-'))
            if packet != last_packet + 1 and packet < last_window_size - 1:  # اگر بسته ای که دریافت کردیم با بسته ای که انتظار داشتیم برابر نبود، یعنی بسته ریجکت شده است
                print(f"Reject Packet {last_frame}-{last_packet + 1}".encode())  # به کلاینت یه Reject Packet می فرستیم
                conn.sendall(f"Reject Packet {last_frame}-{last_packet + 1}".encode())  # به کلاینت یه Reject Packet می فرستیم
                continue
            last_packet = packet
            last_frame = frame
            conn.sendall(f"Accept Packet {frame}-{packet}".encode())  # به کلاینت یه Accept Packet می فرستیم
        except ValueError:
            continue
    conn.close()

if __name__ == "__main__":
    server()
