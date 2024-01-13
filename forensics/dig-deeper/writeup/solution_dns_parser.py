import struct



def get_transaction_id(data):
    data_msg= data[:2]
    id =""
    for byte in data_msg:
        id += hex(byte)[2:]
    
    id = int(id,16)
    return id


def get_flag(data):
    flag={}
    data_msg=data[2:4]

    data=struct.unpack('!H',data_msg)[0]
    
    qr = (data>>15)&int("1",2)
    opcode = (data>>11)&int("1111",2)
    AA = (data>>10)&int("1",2)
    TC = (data>>9)&int("1",2)
    RD = (data>>8)&int("1",2)
    RA = (data>>7)&int("1",2)
    Z = (data>>6)&int("1",2)
    AD = (data>>5)&int("1",2)
    CD = (data>>4)&int("1",2)
    RCODE = (data)&int("1111",2)

    flag['qr'] = qr
    flag['opcode'] = opcode
    flag['aa'] = AA
    flag['tc'] = TC
    flag['rd'] = RD
    flag['ra'] = RA
    flag['z'] = Z
    flag['ad'] = AD
    flag['cd'] = CD
    flag['rcode'] = RCODE

    return flag


def get_count(data):
    
    arr=[]
    for i in range(4,15,2):
        data_count = data[i:i+2]
        count = struct.unpack('!H',data_count)[0]
        arr.append(count)
    return arr

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
    questiontype = data[y:y+2]

    domain_name = ""
    for i in range(0,len(domainparts) - 1):
        if i == len(domainparts) -2:
            domain_name += domainparts[i]
        else :
            domain_name += domainparts[i] +"."
    qtype = struct.unpack('!h',questiontype)[0]
    q_row_3 = data[y+2:y+4]
    qclass = struct.unpack('!h',q_row_3)[0]
    arr.append(domain_name)
    arr.append(qtype)
    arr.append(qclass)
    arr.append(y+4+12+2)
    return arr

def get_answer(data):
    arr=[]
    flag_1 = struct.unpack('!h',data[0:2])[0]
    flag_2 = struct.unpack('!h',data[2:4])[0]
    flag_3 = struct.unpack('!I',data[4:8])[0] 
    flag_4 = struct.unpack('!h',data[8:10])[0]

    arr.append(flag_1)
    arr.append(flag_2)
    arr.append(flag_3)
    arr.append(flag_4)
    data = data[10:14]
    ip =""
    for byte in data:
        pid = hex(byte)[2:]
        pid = int(pid,16)
        ip += str(pid) + "."
    ip = ip[:-1]

    arr.append(ip)
    return arr



def response_parser(response_mesage_raw: bytearray) -> str:
    
    ID = get_transaction_id(response_mesage_raw)
    
    flag = get_flag(response_mesage_raw)
    QR = flag["qr"]
    OPCODE = flag["opcode"]
    AA = flag["aa"]
    TC = flag["tc"]
    RD = flag["rd"]
    RA = flag["ra"]
    AD = flag["ad"]
    CD = flag["cd"]
    RCODE = flag["rcode"]

    count_arr = get_count(response_mesage_raw)
    QDCOUNT=count_arr[0]
    ANCOUNT=count_arr[1]
    NSCOUNT=count_arr[2]
    ARCOUNT=count_arr[3]

    q_arr = get_domain(response_mesage_raw)
    QNAME=q_arr[0]
    QTYPE=q_arr[1]
    QCLASS=q_arr[2]
    q_length = q_arr[3] 
    

    ans_arr = get_answer(response_mesage_raw[q_length:])
    TYPE=ans_arr[0]
    CLASS=ans_arr[1]
    TTL=ans_arr[2]
    RDLENGTH=ans_arr[3] 
    IP=ans_arr[4]

    result = (
    '''
    [Response from DNS Server]\n
    -------------------------------------------------------------------------\n
    HEADERS\n
    Request ID: {}\n
    QR: {} | OPCODE: {} | AA: {} | TC: {} | RD: {} | RA: {} | AD: {} | CD: {} | RCODE: {}\n
    Question Count: {} | Answer Count: {} | Authority Count: {} | Additional Count: {}\n
    -------------------------------------------------------------------------\n
    QUESTION\n
    Domain Name: {} | QTYPE: {} | QCLASS: {}\n
    -------------------------------------------------------------------------\n
    ANSWER
    TYPE: {} | CLASS: {} | TTL: {} | RDLENGTH: {}
    IP Address: {}
    ==========================================================================
    ''').format(ID,QR,OPCODE,AA,TC,RD,RA,AD,CD,RCODE,QDCOUNT,ANCOUNT,NSCOUNT,ARCOUNT,QNAME,QTYPE,QCLASS,TYPE,CLASS,TTL,RDLENGTH,IP)

    return result

def main():
    response =b'\x83\x95\x85\x80\x00\x01\x00\x01\x00\x00\x00\x01\x03ctf\x0214\x08compfest\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\t:\x80\x00\x04\x98vF\x14\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x1c\x00\n\x00\x183K\x05z&\x88\x1e\xf4\x01\x00\x00\x00c6\x98\xba\xa5\x16\xc1TAO%!'
    print(response_parser(response))
    
   
if __name__ == "__main__":
    main() 