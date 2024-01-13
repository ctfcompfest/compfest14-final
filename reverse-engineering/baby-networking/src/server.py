import socket
import threading
import time
from typing import Tuple

SERVER_IP = ""
SERVER_PORT = 4321
BUFFER_SIZE = 1024

def decode(input: str):
    if (input[:4] != "flag"):
        return ""
    inputArr = input[4:].split("_")
    if (len(inputArr) != 4):
        return ""
    name = inputArr[0]
    host = inputArr[1]
    ip = inputArr[2]
    port = inputArr[3]

    ret = ""
    for i in range(min(len(name), len(ip))):
        ret += chr((((ord(name[i])-ord('a'))+(ord(ip[i])-ord('.')))%26)+ord('a'))
    for i in range(min(len(host), len(ip))):
        ret += chr((((ord(host[i])-ord('a'))+(ord(ip[i])-ord('.')))%26)+ord('a'))
    ret += port
    return ret

def logic(input: str):
    if (decode(input) == "gcaeeqwrrgmnvyxgcaevjnlraidvzm11235"):
        return "COMPFEST14{D4ve_heR3_t0ld_mE_tHat_this_chAllenge_1s_tr4sh_cf74de3037}"
    return "Invalid Request"

def socket_handler(connection: socket.socket, address: Tuple[str, int]):
    input_value_bytes = connection.recv(BUFFER_SIZE)
    input_value = input_value_bytes.decode("UTF-8")

    print(f"Receive input from {address}: {input_value}")

    output_value = logic(input_value)
    output_value_bytes = output_value.encode("UTF-8")

    connection.send(output_value_bytes)
    connection.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
        sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sc.bind((SERVER_IP, SERVER_PORT))
        sc.listen(0)

        while True:
            connection, address = sc.accept()

            thread_job = threading.Thread(
                target=socket_handler, args=(connection, address)
            )
            thread_job.start()


if __name__ == "__main__":
    main()
