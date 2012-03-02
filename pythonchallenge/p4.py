# Answer: peak.html
import urllib2, re
url_base = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
number_re = re.compile("the next nothing is (\d+)")

def get_nothing(number):
   return urllib2.urlopen(url_base + number).read()

#next = "12345" - start = 12345
next = str(92118/2)
for i in range(400):
   page = get_nothing(next)
   print page
   next = number_re.findall(page)[0]
