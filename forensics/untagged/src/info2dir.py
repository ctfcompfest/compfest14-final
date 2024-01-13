#!/usr/bin/env python2
import struct
import os

rootdir = 'Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/'
entry_offset = 20

with open(rootdir + 'INFO2', 'rb') as f:
    content = f.read()


def lists(path, mode, exclude=['INFO2', 'desktop.ini']):
    result = []

    for r, d, f in os.walk(path):
        for _ in eval(mode):
            if _ not in exclude:
                abspath = os.path.join(r, _)
                result.append(abspath)

    return result


entries = list()
while entry_offset < len(content):
    entry = content[entry_offset : entry_offset + 800]
    entries.append(entry)
    entry_offset += 800

entries_catalog = dict()
for entry in entries:
    record_id = struct.unpack('<I', entry[260:264])[0]
    basedir = entry[3:260].strip('\x00')
    basedir = basedir.replace('\\', '/')
    
    ext = os.path.splitext(basedir)[1]
    key_path = 'DC%s%s' % (record_id, ext)
    entries_catalog[key_path] = basedir

dir_files = lists(rootdir, 'd') + lists(rootdir, 'f')
for deleted_path in dir_files:
    if not os.path.exists(deleted_path):
        pass

    path = os.path.basename(deleted_path)
    original_path = entries_catalog[path]

    try:
        basedir = os.path.dirname(original_path)
        os.makedirs(basedir)
    except OSError:
        pass
    finally:
        if os.path.isfile(deleted_path):
            with open(deleted_path, 'rb') as f1:
                with open(original_path, 'wb') as f2:
                    f2.write(f1.read())
