# Answer: disproportional ity(crossed out)
#>>> data[0::5][0:100]
#'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\xb4\x00\xb4\x00\x00\xff\xe1\x08\xa4Exif\x00\x00MM\x00*\x00\x00\x00\x08\x00\x00\x00\x00\x00\x0e\x00\x02\x02\x01\x00\x04\x00\x00\x00\x01\x00\x00\x00,\x02\x02\x00\x04\x00\x00\x00\x01\x00\x00\x08p\x00\x00\x00\x00\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x05'
#>>> data[1::5][0:100]
#'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x90\x00\x00\x01,\x08\x02\x00\x00\x00b\xd5r\x95\x00\x00\x00\x06bKGD\x00\x00\x00\x00\x00\x00\xf9C\xbb\x7f\x00\x00\x00\tpHYs\x00\x00\x1b\xaf\x00\x00\x1b\xaf\x01^\x1a\x91\x1c\x00\x00\x00\x07tIME\x07\xd5\x05\x01\x13 ;\xc4\x94\x1f\x86\x00\x00 \x00IDATx'
#>>> data[2::5][0:100]
#'GIF87a@\x01\xf0\x00\xe7\x00\x00\x00\x01\x00\x00\x01\x04\x02\x00\x05\x00\x02\x00\x06\x00\x00\x04\x00\x06\x00\x01\x0e\x00\x03\x06\x01\x04\x00\x00\x04\x07\x05\x02\x07\x00\x05\t\x00\x03\x15\x06\x01\x15\x03\x04\x10\x07\x04\n\x00\x07\x11\x01\x08\x0b\x05\x08\x04\x05\x06\x11\x06\x04\x1b\x02\x07\x17\x00\x08\x1b\x04\x07 \x08\t\x14\x02\x0b\x1d\x06\x0b\x19\x00\r!\x06\n!'
#>>> data[3::5][0:100]
#"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01@\x00\x00\x00\xf0\x08\x02\x00\x00\x00\xfeO*<\x00\x00\x00\tpHYs\x00\x00\x1b\xaf\x00\x00\x1b\xaf\x01^\x1a\x91\x1c\x00\x00\x00\x07tIME\x07\xd5\x05\x01\x13(\t\xc4\x9a\xc4\x0e\x00\x00 \x00IDATx\xda\xec\xbd\xd9\x93\x1d\xd7\x95\xee\xf7}k\xef\x9d\x99'\xcfP"
#>>> data[4::5][0:100]
#'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\xb4\x00\xb4\x00\x00\xff\xe1\x0b\xdfExif\x00\x00MM\x00*\x00\x00\x00\x08\x00\x00\x00\x00\x00\x0e\x00\x02\x02\x01\x00\x04\x00\x00\x00\x01\x00\x00\x00,\x02\x02\x00\x04\x00\x00\x00\x01\x00\x00\x0b\xab\x00\x00\x00\x00\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x05'
#>>> data[5::5][0:100]
#'\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\xb4\x00\xb4\x00\x00\xff\xe1\x08\xa4Exif\x00\x00MM\x00*\x00\x00\x00\x08\x00\x00\x00\x00\x00\x0e\x00\x02\x02\x01\x00\x04\x00\x00\x00\x01\x00\x00\x00,\x02\x02\x00\x04\x00\x00\x00\x01\x00\x00\x08p\x00\x00\x00\x00\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x05\x03'

data = open("evil2.gfx", "rb").read()
exts = ['jpg', 'png', 'gif', 'jpg', 'jpg']
for i in range(len(exts)):
   f = open("evil2_%d.%s" % (i,exts[i]), "wb")
   f.write(data[i::5])
   f.close()