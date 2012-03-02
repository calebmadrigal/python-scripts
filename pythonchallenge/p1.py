# Answer: ocr

code = """g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj. """

def trans_char(c):
   if ord('a') <= ord(c) <= ord('z'):
      num = ord(c)+2
      if num > ord('z'):
         num -= 26  #Wrap-around
      return chr(num)
   else:
      return c

def trans_string(s):
   trans = ""
   for c in s:
      trans += trans_char(c)
   return trans

print trans_string(code)
