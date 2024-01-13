import sys

flag = b"COMPFEST14{m1ps_i3_e4sy_r1gHt???_b868937a70}"
encoder = b"\xc0\xff\xbd\x67"
encoder += b"\x00\x00\xbf\xff"
encoder += b"\x08\x00\xa4\x67"
encoder += b"\x25\x28\x00\x00"
encoder += b"\x2c\x00\x06\x24"
encoder += b"\x60\x80\x99\xdf"
encoder += b"\xf5\x09\x11\x04"
encoder += b"\x00\x00\x00\x00"
encoder += b"\x68\x80\x84\xdf"
encoder += b"\x08\x00\xa5\x67"
encoder += b"\x70\x80\x99\xdf"

encrypted = []
for i in range(len(flag)):
    encrypted.append(flag[i]^encoder[i])

sys.stdout.buffer.write(bytes(bytearray(encrypted)))
