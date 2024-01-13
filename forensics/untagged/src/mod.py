#!/usr/bin/env python2
import struct
import sys
import re

rule = re.compile(r'(PK.*?)(?=PK)', re.S)
eof = re.compile(r'PK.+(PK.+?)$', re.S)

def pack(num, length=2):
    if length == 2:
        return struct.pack('<H', num)

    elif length == 4:
        return struct.pack('<I', num)

with open(sys.argv[1], 'rb') as f:
    content = f.read()

matches = rule.findall(content)
endzip = eof.findall(content)[0]

# Exclude all files except INFO2 from Central Directory Header
offset = len(matches)/2
exclude = re.compile(r'(INFO2)', re.S)
exclude2 = re.compile(r'(\/DC\d+\.?\w*)\n', re.S)

count = offset
temp = ''

for i in range(offset, len(matches)):
    m = matches[i]

    if not exclude.search(m):
        if exclude2.findall(m):
            content = content.replace(m, '')
            count -= 1
        else:
            temp += m
    else:
        temp += m

n_endzip = endzip[:8] + pack(count) + pack(count) + pack(len(temp), 4) + endzip[16:]
content = content.replace(endzip, n_endzip)

with open(sys.argv[2], 'wb') as f:
    f.write(content)
