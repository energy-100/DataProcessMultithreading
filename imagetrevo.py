out_path = r'C:/Users/ENERGY/Desktop/testdata/'

index = 1

def getkey(f):
    global index
    dat_read = open(f, "rb")
    out = out_path
    for key in range(1):
        out = out_path+str(key)+'outimage.jpg'
        png_write = open(out, "wb")
        print('png_write',png_write)
        print(index, f)
        index += 1
        for now in dat_read:
            for nowByte in now:
                # print('nowByte',nowByte)
                # print(type(key))
                # print(key)
                newByte = nowByte ^ 0x6a
                # newByte = nowByte ^ int(str(key),2)
                png_write.write(bytes([newByte]))



def imageDecode(f):
    global index
    dat_read = open(f, "rb")
    # out='P:\\'+fn+".png"
    out = out_path
    for key in range(1):
        out = out_path+str(key)+'outimage.jpg'
        png_write = open(out, "wb")
        print('png_write',png_write)
        print(index, f)
        index += 1
        for now in dat_read:
            for nowByte in now:
                # print('nowByte',nowByte)
                # print(type(key))
                # print(key)
                newByte = nowByte ^ 0x05
                # newByte = nowByte ^ int(str(key),2)
                png_write.write(bytes([newByte]))
        png_write.close()
# # imageDecode(r"C:\Users\ENERGY\Desktop\testdata\bc4040b6b1b02ede5c7677127e390d5a.dat")
# ,'\x40','\x40','\xb6','\xb1','\xb0','\x2e','\xde','\x5c','\x76','\x77','\x12','\x7e','\x39','\x0d','\x5a')
# print(hex(int('bc4040b6b1b02ede5c7677127e390d5a',2)^ 0x05))
# print(int(str(int('bc4040b6b1b02ede5c7677127e390d5a',16)^ 0x05),16))
# # print(('bc4040b6b1b02ede5c7677127e390d5a').encode('utf-8'))