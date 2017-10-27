# coding=u8

import random

def recreate(imgPath):
    with open(imgPath, 'rb') as f1:
        bin = f1.read()
    bin = bytearray(bin)
    bin = bin[:-2] + str(random.randint(0,9)) + str(random.randint(0,9))
    with open(imgPath, 'wb') as f2:
        f2.write(bin)