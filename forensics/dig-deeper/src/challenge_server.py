import socket
import struct
import random

from typing import Tuple

def main():
    port = 3534 
    ip = ''
    dns_ip = '8.8.8.8'
    dns_port = 53
    dns_addr =(dns_ip,dns_port) 
    sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    BUFFER_SIZE = 2048
    sc.bind((ip, port))

     # ip :152.118.70.20 & id:39061
    result_1=b'\x98\x95\x85\x80\x00\x01\x00\x01\x00\x00\x00\x01\x03ctf\x0214\x08compfest\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04\x98vF\x14\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x1c\x00\n\x00\x183K\x05z&\x88\x1e\xf4\x01\x00\x00\x00c6\x98\xba\xa5\x16\xc1TAO%!'
    # ip :152.118.70.20 & id:33685
    result_2=b'\x83\x95\x85\x80\x00\x01\x00\x01\x00\x00\x00\x01\x03ctf\x0214\x08compfest\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04\x98vF\x14\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x1c\x00\n\x00\x183K\x05z&\x88\x1e\xf4\x01\x00\x00\x00c6\x98\xba\xa5\x16\xc1TAO%!'
    # ip :152.118.70.20 & id:17189
    result_3=b'\x43\x25\x85\x80\x00\x01\x00\x01\x00\x00\x00\x01\x03ctf\x0214\x08compfest\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04\x98vF\x14\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x1c\x00\n\x00\x183K\x05z&\x88\x1e\xf4\x01\x00\x00\x00c6\x98\xba\xa5\x16\xc1TAO%!'
    # ip :152.118.70.20 & id:4645
    result_4=b'\x12\x25\x85\x80\x00\x01\x00\x01\x00\x00\x00\x01\x03ctf\x0214\x08compfest\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04\x98vF\x14\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x1c\x00\n\x00\x183K\x05z&\x88\x1e\xf4\x01\x00\x00\x00c6\x98\xba\xa5\x16\xc1TAO%!'
    # ip :152.118.70.20 & id:21365
    result_5=b'\x53\x75\x85\x80\x00\x01\x00\x01\x00\x00\x00\x01\x03ctf\x0214\x08compfest\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04\x98vF\x14\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x1c\x00\n\x00\x183K\x05z&\x88\x1e\xf4\x01\x00\x00\x00c6\x98\xba\xa5\x16\xc1TAO%!'

    result_list = [result_1,result_2,result_3,result_4,result_5]

    while True:
        data_client, client_addr = sc.recvfrom(BUFFER_SIZE)
        domain_name = get_domain(data_client)        
        
        if domain_name == "ctf.14.compfest":
            num = random.randint(0,4)
            sc.sendto(result_list[num], client_addr)
        else:    
            sc.sendto(data_client, dns_addr)
            data,addr = sc.recvfrom(BUFFER_SIZE)
            sc.sendto(data,client_addr)


def get_domain(data):
    arr =[]
    data = data[12:]
    state = 0
    expectedlength = 0
    domainstring = ''
    domainparts = []
    x = 0
    y = 0
    for byte in data:
        if state == 1:
            if byte != 0:
                domainstring += chr(byte)
            x += 1
            if x == expectedlength:
                domainparts.append(domainstring)
                domainstring = ''
                state = 0
                x = 0
            if byte == 0:
                domainparts.append(domainstring)
                break
        else:
            state = 1
            expectedlength = byte
        y += 1
    
    domain_name = ""
    for i in range(0,len(domainparts) - 1):
        if i == len(domainparts) -2:
            domain_name += domainparts[i]
        else :
            domain_name += domainparts[i] +"."
    
    return domain_name

# DO NOT ERASE THIS PART!
if __name__ == "__main__":
    main() 