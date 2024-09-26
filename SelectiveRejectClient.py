# کلاینت
import socket
import time
import random
import threading


def send_packets(client_socket, start_frame, start_packet, stop_event):
    for frame in range(start_frame, 3):  # فرض کنید تعداد پنجره ها 3 است
        window_size = random.choice([5, 10, 15])  # سایز پنجره به صورت تصادفی انتخاب می‌شود
        start_time = time.time()
        for packet in range(start_packet, window_size):  # هر پنجره شامل window_size بسته است
            if stop_event.is_set():
                break
            client_socket.sendall(f"{frame}-{packet}-{window_size}".encode())
            time.sleep(1)  # فرض کنید زمان ارسال هر بسته 1 ثانیه است
        print(f"Time taken to send a window of size {window_size}: {time.time() - start_time} seconds")


def receive_packets(client_socket, stop_event):
    while True:
        try:
            data = client_socket.recv(1024)
            print(data.decode())
            if "Reject Packet" in data.decode() or "Accept Packet" not in data.decode():
                stop_event.set()  # اگر بسته ای که دریافت کردیم یک Reject Packet بود یا بسته Accept نشده بود، ترد ارسال کننده را متوقف می‌کنیم
                break
            elif "Request Packet" in data.decode():
                frame, packet = map(int, data.decode().split('-'))
                threading.Thread(target=send_packets, args=(client_socket, frame, packet, stop_event)).start()
        except socket.timeout:
            print("No data received for more than 5 seconds.")
            client_socket.sendall("Poll Request".encode())
            data = client_socket.recv(1024)
            frame, packet = map(int, data.decode().split('-'))
            threading.Thread(target=send_packets, args=(client_socket, frame, packet, stop_event)).start()


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    client_socket.connect(('localhost', 12345))
    stop_event = threading.Event()

    threading.Thread(target=send_packets, args=(client_socket, 0, 0, stop_event)).start()
    threading.Thread(target=receive_packets, args=(client_socket, stop_event)).start()  # client_socket.close()


if __name__ == "__main__":
    client()
