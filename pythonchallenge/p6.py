# Answer: hockey.html -> oxygen.html
# Nneeded hint: download channel.zip, "now there are pairs" 
# made me think of the python zip function, and threw me off.
# Needed hint for how to get comments on each file (I downloaded zip and resaved (using archive viewer),
# which erased comments - so I had to re-download it.
import re
import zipfile

z = zipfile.ZipFile("channel.zip", "r")
number_re = re.compile("Next nothing is (\d+)")

def get_nothing(number):
   return z.read(number+".txt")
   #return open("p6/" + number + ".txt", "r").read()

next = "90052"
nodes = []
for i in range(909):
   nodes.append(next)
   page = get_nothing(next)
   print "i =", i, "->", page

   try:
      next = number_re.findall(page)[0]
   except IndexError:
      break

print ''.join([z.getinfo(i+'.txt').comment for i in nodes])
