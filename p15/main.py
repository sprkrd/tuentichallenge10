#!/usr/bin/env python3

import tarfile
import zlib

filename = "animals.tar.gz"

archive = tarfile.open(filename, "r:gz")


# # member = archive.getmember("animals/./admiral0000")
# # member = archive.getmember("animals/./toucan0000")
# member = archive.getmember("animals/./shrew0000")
# # member = archive.getmember("animals/./anaconda0000")

reader = archive.extractfile("animals/./butterfly0000")

buff = reader.read(1024*1024*1024)
while buff:
    if any(buff):
        print("The file contains non-null char")
        break
    buff = reader.read(1024*1024*1024)


# print(reader.read(64))
# print(reader.read(64))
# print(reader.read(64))

# input()

# print(archive.getmembers()[1])


