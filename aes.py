#!/usr/bin/python
import binascii
from copy import copy
import sys

def stringToTab(text):
        byteStringTab = []
        for x in range(len(text)):
                byteStringTab.append(text[x])
        return byteStringTab

def pad(text,sizeOfBytes):
        l = len(text)
        if l % sizeOfBytes > 0:
                delta = sizeOfBytes - (l% sizeOfBytes)
                text = text + bytearray([delta]*delta)
        return stringToTab(text+bytearray())

def unpad(text,sizeOfBytes):
        nl = len(text)
        val = int(binascii.hexlify(str(text[-1])), 16)
        if val > sizeOfBytes:
                return text
        l = nl - val
        return text[:l]

def addRoundKey(text,key):
        i = 0
        key = hexToInt(key)
        while i < 4 :
                j = 0
                while j < 4:
                        text[i][j] = text[i][j]^key[i][j]
                        j=j+1
                i = i+1
        return text
def intToBin(text):
        tmp = []
        i = 0
        while i<4:
                j = 0
                tmp2 = []
                while j< 4:
                        tmp2.append(bin(text[i][j])[2:])
                        j=j+1
                tmp.append(tmp2)
                i = i+1
        return tmp
def binToHex(text):
        tmp = []
        i = 0
        while i<4:
                j = 0
                tmp2 = []
                while j< 4:
                        tmp2.append(hex(int(text[i][j],2)))
                        j=j+1
                tmp.append(tmp2)
                i = i+1
        return tmp

def intToHex(text):
        tmp = []
        i = 0
        while i<4:
                j = 0
                tmp2 = []
                while j< 4:
                        tmp2.append(hex(text[i][j]))
                        j=j+1
		tmp.append(tmp2)
                i = i+1
        return tmp
def hexToInt(text):
        tmp = []
        i = 0
        while i<4:
                j = 0
                tmp2 = []
                while j< 4:
                        tmp2.append(int(text[i][j],16))
                        j=j+1
                tmp.append(tmp2)
                i = i+1
        return tmp
def splitHex(integer):
    return divmod(integer, 0x10)

def subBytes(text):
        tmp = []
        i = 0
        while i<4:
                j = 0
                tmp2 = []
                while j< 4:
                        high, low = splitHex(int(text[i][j]))
                        tmp2.append(sbox[high][low])
                        j=j+1
                tmp.append(tmp2)
                i = i+1
        return tmp

def intToHexOne(char):
        tmp = ""
        if char == 0:
                tmp ="0"
        elif char == 1:
                tmp ="1"
        elif char == 2:
                tmp ="2"
        elif char == 3:
                tmp ="3"
        elif char == 4:
                tmp ="4"
        elif char == 5:
                tmp ="5"
        elif char == 6:
                tmp ="6"
        elif char == 7:
                tmp ="7"
        elif char == 8:
                tmp ="8"
        elif char == 9:
                tmp ="9"
        elif char == 10:
                tmp ="a"
        elif char == 11:
                tmp ="b"
        elif char == 12:
                tmp ="c"
        elif char == 13:
                tmp ="d"
        elif char == 14:
                tmp ="e"
        elif char == 15:
                tmp ="f"
        return tmp
def subBytesInv(text):
        tmp = []
 	i = 0
        column = 0
        line = 0
        while i<4:
                j = 0
                tmp2 = []
                while j< 4:
                        l = 0
                        while l < 16:
                                c = 0
                                while c < 16:
                                        if(text[i][j] == hex(sbox[l][c])):
                                                column = c
                                                line = l
                                                #print"trouve : {} colonne {}  ligne {}".format(text[i][j],column,line)
                                        c = c+1
                                l = l +1
                        #print "line : {}  colonne : {}".format(line, column)
                        tmpstr = "0x"+str(intToHexOne(line))+str(intToHexOne(column))
                        #print "tmpstr : {}".format(tmpstr)
                        tmp2.append(tmpstr)
                        j=j+1
                tmp.append(tmp2)
                i = i+1
        return tmp

def shiftRows(text):
        i = 1
        while i <4:
                n = 0
                while n < i:
                        j = 0
                        while j < 3 :
                                tmp = text[i][j]
                                text[i][j] = text[i][j+1]
                                text[i][j+1] = tmp
                                j = j+1
                        n = n+1
                i = i+1
        return text

def shiftRowsInv(text):
        i = 1
        while i <4:
                n = 0
                while n < i:
                        j = 3
                        while j > 0 :
                                tmp = text[i][j-1]
                                text[i][j-1] =text[i][j]
                                text[i][j] = tmp
                                j = j-1
                        n = n+1
                i = i+1
        return text

def galoisMult(a, b):
        p = 0
        hiBitSet = 0
        for i in range(8):
                if b & 1 == 1:
                        p ^= a
                hiBitSet = a & 0x80
                a <<= 1
                if hiBitSet == 0x80:
                        a ^= 0x1b
                b >>= 1
        return p % 256
def mixColumn(column):
        temp = copy(column)
        column[0] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ galoisMult(temp[2],1) ^ galoisMult(temp[1],3)
        column[1] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ galoisMult(temp[3],1) ^ galoisMult(temp[2],3)
        column[2] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ galoisMult(temp[0],1) ^ galoisMult(temp[3],3)
        column[3] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ galoisMult(temp[1],1) ^ galoisMult(temp[0],3)

def mixColumnInv(column):
        temp = copy(column)
        column[0] = galoisMult(temp[0],14) ^ galoisMult(temp[3],9) ^ galoisMult(temp[2],13) ^ galoisMult(temp[1],11)
        column[1] = galoisMult(temp[1],14) ^ galoisMult(temp[0],9) ^ galoisMult(temp[3],13) ^ galoisMult(temp[2],11)
        column[2] = galoisMult(temp[2],14) ^ galoisMult(temp[1],9) ^ galoisMult(temp[0],13) ^ galoisMult(temp[3],11)
        column[3] = galoisMult(temp[3],14) ^ galoisMult(temp[2],9) ^ galoisMult(temp[1],13) ^ galoisMult(temp[0],11)

def mixColumns(state):
        state = hexToInt(state)
        for i in range(4):
                column = []
                column.append(state[0][i])
                column.append(state[1][i])
                column.append(state[2][i])
                column.append(state[3][i])
                mixColumn(column)
                for j in range(4):
                        state[j][i] = column[j]
        return state

def mixColumnsInv(state):
        state = hexToInt(state)
        for i in range(4):
                column = []
                column.append(state[0][i])
                column.append(state[1][i])
                column.append(state[2][i])
                column.append(state[3][i])
                mixColumnInv(column)
                for j in range(4):
                        state[j][i] = column[j]
        return state

def aes_encrypt(text,sizeOfBytes,key):
        textEncrypted =""
        count = 0
        text = pad(text,sizeOfBytes)
        i = 0
        nb = 0
        while nb < len(text)/16:
                tmptext = []
                i = nb *16
                j = 0
                while j < 4 :
                        tmp = []
                        n = 0
                        while n < 4:
                                tmp.append(text[i])
                                n = n+1
                                i= i+1
                        tmptext.append(tmp)
                        j = j+1
                #print "text before addRound {}".format(tmptext)
                #tmptext = intToBin(tmptext)
                #print tmptext
                #tmptext = binToHex(tmptext)
                #print tmptext
                tmptext = addRoundKey(tmptext,key)
                #print "text after addRound {}".format(tmptext)
                for n in range(9):

                	#tmptext = intToHex(tmptext)
                     	tmptext = subBytes(tmptext)
                        #print "After subBytes : {} ".format(intToHex(tmptext))
                        #tmptext = subBytesInv(intToHex(tmptext))
                        #print "After subBytesInv : {} ".format(tmptext)
                        #tmptext = subBytes(hexToInt(tmptext))
                        #print "intToHex : {}".format(tmptext)
                        #print "Before shiftrows : {} ".format(tmptext)
                        tmptext = shiftRows(intToHex(tmptext))
                        #print "After shiftrows : {} ".format(tmptext)
                        #tmptext = shiftRowsInv(tmptext)
                        #print "After shiftrowsInv : {} ".format(tmptext)
                        #tmptext = shiftRows(tmptext)
                        tmptext = mixColumns(tmptext)
                        tmptext = mixColumnsInv(intToHex(tmptext))
                        tmptext = mixColumns(intToHex(tmptext))
                        #print "After mix : {} ".format(tmptext)
                        tmptext = addRoundKey(tmptext,key)
                        #print "text after addRound {}".format(tmptext)
                tmptext = subBytes(tmptext)
                tmptext = intToHex(tmptext)
                tmptext = shiftRows(tmptext)
                tmptext = hexToInt(tmptext)
                tmptext = addRoundKey(tmptext,key)
                tmptext = intToHex(tmptext)
                for o in range(4):
                        for u in range(4):
                                textEncrypted = textEncrypted + tmptext[o][u]+"&"
                nb = nb+1
        return textEncrypted

def aes_decrypt(text,sizeOfBytes,key):
        textDecrypted =""
        count = 0
        i = 0
        nb = 0
        while nb < len(text)/16:
                tmptext = []
                i = nb *16
                j = 0
                while j < 4 :
                        tmp = []
                        n = 0
                        while n < 4:
                                tmp.append(text[i])
                                n = n+1
                                i= i+1
                        tmptext.append(tmp)
                        j = j+1
                tmptext = addRoundKey(hexToInt(tmptext),key)
                #print "text after addRound {}".format(tmptext)
                for n in range(9):
                        tmptext = shiftRowsInv(tmptext)
                        tmptext = subBytesInv(intToHex(tmptext))
                        tmptext = addRoundKey(hexToInt(tmptext),key)
                        tmptext = mixColumnsInv(intToHex(tmptext))

                #print "text before addRound {}".format(tmptext)
                #tmptext = intToBin(tmptext)
                #print tmptext
                #tmptext = binToHex(tmptext)
                #print tmptext
                #print "text after addRound {}".format(tmptext)
                tmptext = shiftRowsInv(tmptext)
                tmptext = subBytesInv(intToHex(tmptext))
                tmptext = addRoundKey(hexToInt(tmptext),key)
                tmptext = intToHex(tmptext)
                for o in range(4):
                        for u in range(4):
                                textDecrypted = textDecrypted + tmptext[o][u]
		nb = nb+1
        return textDecrypted
def hexToAscii(text):
	textSplit = text.split("0x")
	tmpText = ""
	#print textSplit
	for hexa in textSplit:
		if hexa !=  "":
			if len(hexa) != 1:
				tmpText = tmpText + str(hexa.decode("hex"))
			elif hexa == 'a':
				tmpText = tmpText+ "\n"
	return tmpText

sbox = [
   [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
   [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
   [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
   [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
   [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
   [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
   [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
   [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
   [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
   [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
   [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
   [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
   [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
   [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
   [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
   [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
   ]

key =[["0x78","0x76","0x11","0xBB"],
      ["0xA8","0xB3","0x41","0xAA"],
      ["0xCA","0x51","0xC5","0x65"],
      ["0x61","0xFF","0xEA","0xD1"]]
sizeOfBytes = 16

count = 0
server = 0;
if sys.argv[2] == "-s":
	server = 1;
if sys.argv[1] == "-e":
	if server  == 1:
		ftext = open("/root/workspace/client-server/text.txt","r")
	else:
		ftext = open("/root/workspace/client-server/textC.txt","r")
	text = ftext.read()
	#print "text a chiffrer : {}".format(text)
	if server == 1:
		ftextEncrypted = open("/root/workspace/client-server/textEncrypted.txt","wb")
	else:
		ftextEncrypted = open("/root/workspace/client-server/textEncryptedC.txt","wb")
	textEncrypted = aes_encrypt(text,sizeOfBytes,key)
	ftextEncrypted.write(textEncrypted)
	#print "text chiffre : {}".format(textEncrypted)

elif sys.argv[1] == "-d":
	if server == 1:
		ftextEncrypted = open("/root/workspace/client-server/textEncrypted.txt","r")
	else:
		ftextEncrypted = open("/root/workspace/client-server/textEncryptedC.txt","r")
	textEncrypted = ftextEncrypted.read()
	#print "text Ecrypted : {}".format(textEncrypted)
	if server  == 1:
		ftextDecrypted = open("/root/workspace/client-server/textDecrypted.txt","wb")
	else:
		ftextDecrypted = open("/root/workspace/client-server/textDecryptedC.txt","wb")
	textDecrypted = aes_decrypt(textEncrypted.split('&')[:-1],sizeOfBytes,key)
	#print "text dechiffre : {}".format(textDecrypted)
	textDecryptedHexToAscii = hexToAscii(textDecrypted)
	#print "text dechiffre hex to ascii : {}".format(textDecryptedHexToAscii)
	ftextDecrypted.write(textDecryptedHexToAscii)
#print text
