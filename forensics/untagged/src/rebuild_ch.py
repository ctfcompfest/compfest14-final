from calendar import timegm

import datetime
import struct
import sys
import re

rule = re.compile(rb'(PK.*?)(?=PK)', re.S)
eof = re.compile(rb'PK.+(PK.+?)$', re.S)

EPOCH_AS_FILETIME = 116444736000000000
HUNDREDS_OF_NANOSECONDS = 10000000


def unpack(data, mode='<H'):
    return struct.unpack(mode, data)[0]

def pack(number, mode='<H'):
    return struct.pack(mode, number)


class UTC(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.imedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)


class UTCDOSTime(object): # Convert 4-bytes DOSTime into UTC Epoch-timestamp

    @staticmethod
    def date_to_time(data):
        dostime = unpack(data,'<I')
        dt = datetime.datetime(
            (((dostime >> 25) & 0x7f) + 1980),
            ((dostime >> 21) & 0x0f),
            ((dostime >> 16) & 0x1f),
            ((dostime >> 11) & 0x1f),
            ((dostime >> 5) & 0x3f),
            ((dostime << 1) & 0x3e)
        )

        if (dt.tzinfo is None) or (dt.tzinfo.utcoffset(dt) is None):
            dt = dt.replace(tzinfo=UTC())
    
        return EPOCH_AS_FILETIME + (timegm(dt.timetuple()) * HUNDREDS_OF_NANOSECONDS)


class LocalHeader(object): # First part of Zip, contain general information of file/directory + file_data 
    def __init__(self, raw):
        self.raw = raw
        
        self.signature = raw[:4]
        self.version_extract = raw[4:6]
        self.bit_flag = raw[6:8]
        self.compression_method = raw[8:10]
        self.last_mod_time = raw[10:12]
        self.last_mod_date = raw[12:14]
        self.uncompressed_crc_data = raw[14:18]
        self.compressed_size = raw[18:22]
        self.uncompressed_size = raw[22:26]
        self.filename_len = raw[26:28]
        self.extra_field_len = raw[28:30]

        self.filename = self.get_filename()
        self.extra_field = self.get_extra_field()
        self.file_data = self.get_file_data()

    def get_filename(self):
        name_offset = 30 + unpack(self.filename_len)
        return self.raw[30: name_offset]

    def get_extra_field(self):
        name_offset = 30 + unpack(self.filename_len)
        extra_offset = unpack(self.extra_field_len)

        return self.raw[name_offset:name_offset+extra_offset]

    def get_file_data(self):
        file_offset = 30 + len(self.filename) + len(self.extra_field)
        return self.raw[file_offset:]

    def get_localheader_offset(self):
        return pack(content.find(self.raw), '<I')


class ExtraField(LocalHeader): # Extra field for Local/Central Header. Currently only applicable for FileTimes field
    def __init__(self, raw):
        super().__init__(raw)

    def get_time(self):
        return UTCDOSTime.date_to_time(
            self.last_mod_time + self.last_mod_date
        )

    @property
    def length(self):
        return pack(36)

    @property
    def field_id(self):
        return b'\x0a\x00' # NTFS FileTimes

    @property
    def field_length(self):
        return pack(32)

    @property
    def reserved(self):
        return pack(0, '<I')

    @property
    def tag(self):
        return pack(1)

    @property
    def size(self):
        return pack(24)

    @property
    def mtime(self):
        return pack(self.get_time(), '<Q')

    @property
    def ctime(self):
        return pack(self.get_time(), '<Q')

    @property
    def atime(self):
        return pack(self.get_time(), '<Q')

    @property
    def content(self):
        return (
            self.field_id
          + self.field_length
          + self.reserved
          + self.tag
          + self.size
          + self.mtime
          + self.ctime
          + self.atime
        )


class CentralHeader(LocalHeader): # 2nd part of Zip, contain reference of Local Header alongwith its file_data
    def __init__(self, raw):
        super().__init__(raw)

        self.signature = b'\x50\x4b\x01\x02'
        self.version_made = b'\x3f\x03'
        self.version_extract = b'\x14\x03'
        self.disk_number = b'\x00\x00'
        
        self.file_comment = b''
        self.file_comment_len = pack(len(self.file_comment))

        self.internal_file_attr = self.get_internal_file_attr()
        self.external_file_attr = self.get_external_file_attr()

        self.extra_field = ExtraField(raw).content
        self.extra_field_len = ExtraField(raw).length 

        self.localheader_offset = self.get_localheader_offset()

    def get_internal_file_attr(self):
        return b'\x00\x00' # 0 for Binary-Data, Otherwise 1 for Text/ASCII-Data

    def get_external_file_attr(self):
        if self.get_file_data(): # If local header has file_data then it's a file
            return b'\x20\x80\xb4\x81'

        return b'\x10\x80\xfd\x41' # Otherwise, it's a directory


    @property
    def content(self):
        return (
            self.signature + self.version_made + self.version_extract
          + self.bit_flag + self.compression_method + self. last_mod_time
          + self.last_mod_date + self.uncompressed_crc_data + self.compressed_size
          + self.uncompressed_size + self.filename_len + self.extra_field_len + self.file_comment_len
          + self.disk_number + self.internal_file_attr + self.external_file_attr + self.localheader_offset
          + self.filename + self.extra_field + self.file_comment
          
        )


class EndCentralHeader(object): # End of Zip, contain total entries & offset/size to central_header
    def __init__(self, total_entries, central_header_size, central_header_offset):
        self.signature = b'\x50\x4b\x05\x06'
        self.disk_number = b'\x00\x00'
        self.disk_central_dir_number = b'\x00\x00'
        self.disk_entries = pack(total_entries)
        self.total_entries = pack(total_entries)
        self.central_header_size = pack(central_header_size, '<I')
        self.central_header_offset = pack(central_header_offset, '<I')
        self.file_comment_len = b'\x00\x00'


    @property
    def content(self):
        return (
            self.signature + self.disk_number + self.disk_central_dir_number
          + self.disk_entries + self.total_entries + self.central_header_size
          + self.central_header_offset + self.file_comment_len
        )


with open(sys.argv[1], 'rb') as f:
    content = f.read()

matches = rule.findall(content)
for e, m in enumerate(matches):
    if not LocalHeader(m).filename:
        break

num_of_entries = e
local_headers = matches[ :num_of_entries]

local_header = b''.join(local_headers)
central_header = b''

for header in local_headers:
    Header = CentralHeader(header)
    central_header += Header.content

end_central_header = EndCentralHeader(
    num_of_entries,
    len(central_header),
    len(local_header)
).content

with open(sys.argv[1][:-4] + '_fixed.zip', 'wb') as f:
    result = local_header + central_header + end_central_header
    f.write(result)
