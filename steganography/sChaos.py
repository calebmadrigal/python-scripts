#!/usr/bin/python
#
# Written: 2003
#
# sChaos 1.2 is a steganography reader/writer written by Caleb Madrigal
# Use sChaos to hide any type of file inside of a 24-bit bitmap file
#
# Note: I wrote this program back in high school, so it is not very well written :)
#       But it does do its job well.

import sys

#=======FUNCTIONS=======#
def getbits(char):
    bits=[0,0,0,0,0,0,0,0]
    i=7
    num=ord(char)
    while (num > 0):
      bits[i]=num%2
      num/=2
      i-=1
    return bits

def getbyte(bits):
    sum=0
    for i in range(8):
        sum+=(bits[i]*(2**(7-i)))
    return chr(sum)

def getlsb(char):
    return (ord(char)%2)

def hidebyte(input, output, plainchar):
    bits=getbits(plainchar)
    for i in range(8):
	output.write(chr((ord(input.read(1))&254)+bits[i]))

def extractbyte(stream, bmchars):
    bits=[]
    for i in range(8):
        bits.append(getlsb(bmchars[i]))
    stream.write(getbyte(bits))

def writeheader(input, output):
    output.write(input.read(54))


def putsize(input, output, data):
    bytes=[]
    bytes.append(chr((len(data)>>16) & 255))
    bytes.append(chr((len(data)>>8) & 255))
    bytes.append(chr(len(data) & 255))

    for i in range(3):
        hidebyte(input, output, bytes[i])

def getsize(stream):
    stream.seek(54)
    sum=0
    for i in range(3):
        bits=[]
        for j in range(8):
            bits.append(getlsb(stream.read(1)))
        sum+=ord(getbyte(bits))<<(8*(2-i))
    return sum

def getfilesize(stream):
    content=stream.read()
    stream.seek(0)
    length=len(content)
    del content
    return length

def findspace():
    bitmap=(raw_input("Bitmap file: "))
    try:
        bmp=file(bitmap,"r")
        space=bmp.read()
        bmp.close()
        print (len(space)-54)/(8*1024), "kilobytes available in", bitmap, "\n"
    except IOError:
        print "\nBad file name"
        sys.exit(1)


def hide():
    infile=(raw_input("Input file to hide in bitmap: "))
    input=(raw_input("Input bitmap file           : "))
    output=(raw_input("Output name of bitmap       : "))

    try:
        infile=file(infile,"r")
        input=file(input,"r")
        output=file(output,"w")
        
    except IOError:
        print "\nBad file name(s)"
        sys.exit(1)

    plain=infile.read()
    infile.close()

    print "\nHiding", len(plain), "byte file..."

    bmsize=getfilesize(input)

    if (bmsize/8)+24 >= len(plain):
        writeheader(input, output)
        putsize(input, output, plain)
        for i in range(len(plain)):
            hidebyte(input, output, plain[i])
        for j in range(((bmsize)-i)):
            output.write(input.read(1))
    print "Done\n"

def extract():
    input=(raw_input("Bitmap with hidden file: "))
    output=(raw_input("Output file            : "))

    try:
        input=file(input, "r")
        output=file(output, "w")

    except IOError:
        print "\nBad file name(s)"
        sys.exit(1)

    size=getsize(input)
    print "\nExtracting", size, "byte file..."
    
    for i in range(size):
        bits=[0,0,0,0,0,0,0,0]
        for j in range(8):
            bits[j]=getlsb(input.read(1))
        output.write(getbyte(bits))
    print "Done\n"


print "============================="
print "= sChaos Stegenography tool ="
print "=     by Caleb Madrigal     ="
print "=============================\n"

print "1 -> Hide a file in a bitmap"
print "2 -> Extract a file from a bitmap"
print "3 -> Find potential space in a bitmap file\n"

valid=0
while valid!=1:
    mode=(raw_input("(1, 2, 3) >> "))
    if mode=="1" or mode=="2" or mode=="3":
        valid=1

if mode=="1":
    hide()
if mode=="2":
    extract()
if mode=="3":
    findspace()
