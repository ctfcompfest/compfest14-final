import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4321
BUFFER_SIZE = 1024


def main():
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect((SERVER_IP, SERVER_PORT))

    print("Contoh Socket Client TCP")
    print("Tekan Ctrl/CMD+C untuk menghentikan program")

    input_value = input("Masukan sebuah string untuk dikirimkan ke server: ")
    input_value_bytes = input_value.encode("UTF-8")

    sc.send(input_value_bytes)

    output_value_bytes = sc.recv(BUFFER_SIZE)
    output_value = output_value_bytes.decode("UTF-8")

    print(f"Balasan dari server {(SERVER_IP, SERVER_PORT)}: {output_value}")

    sc.close()


if __name__ == "__main__":
    main()