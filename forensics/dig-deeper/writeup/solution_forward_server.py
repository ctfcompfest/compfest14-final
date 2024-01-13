import socket

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



port = 9903 
ip = ''
ip_server = '34.69.100.193' #ip server
port_server = 3534 # port server
BUFFER_SIZE = 2048
server_addr = (ip_server,port_server)

sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sc.bind((ip, port))

while True:

    data_client, client_addr = sc.recvfrom(BUFFER_SIZE)
    sc.sendto(data_client, server_addr)

    domain = get_domain(data_client)

    data_server, ip_asdos = sc.recvfrom(BUFFER_SIZE)

    
    print(data_server)
    sc.sendto(data_server,client_addr)
