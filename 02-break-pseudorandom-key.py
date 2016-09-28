def strxor(a, b):     # xor two strings (trims the longer input)
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

# convert an integer to 8-bit 2's complement binary number
def toBinary(n):
    return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])

# get a number generated from 4 key characters with binary and bit manipulation
def getkey(c0, c1, c2, c3):
    return int(toBinary(ord(c3)) + toBinary(ord(c2)) + toBinary(ord(c1)) + toBinary(ord(c0)), 2)

# get the ith byth of an integer
def byte(n, i):
    return int(''.join(str(1 & int(n) >> i) for i in range(32)[::-1])[32-(i+1)*8:32-i*8], 2)

def nextkey(prevkey):
    return (prevkey * 1103515245 + 12345) % (2**31)

with open('hw2.tex.enc', 'r') as f:
    content = f.read()
    length = len(content)
    txt = "%%%%%%%%%%%%"    # guessed first characters of the file
    plaintxt = ""

    key = strxor(content, txt)
    # convert the 'key' to numbers every 4 characters
    randints = []

    for i in range(len(key)/4):
        # randints.append(getkey(key[i * 4 +3], key[i * 4 + 2], key[i * 4 + 1], key[i * 4]))  # big-endianess
        randints.append(getkey(key[i * 4], key[i * 4 + 1], key[i * 4 + 2], key[i * 4+3]))  # little-endianess (works on MAC)

    for j in range(len(content) - len(txt)):
        key = strxor(content[j:], txt)
        # convert get the first randomly generated integers
        randints = []
        for i in range(len(key) / 4):
            randints.append(getkey(key[i * 4], key[i * 4 + 1], key[i * 4 + 2], key[i * 4 + 3]))
        if len(randints) >= 2 and randints[1] == nextkey(randints[0]):  # guess correctly here!
            #   decrypt from index j
            while len(randints) < length / 4 + 1:
                randints.append(nextkey(randints[-1]))
            for i in range(j, len(content)):
                plaintxt += chr(ord(content[i]) ^ (byte(randints[i / 4], i % 4)))
            break
    print plaintxt
