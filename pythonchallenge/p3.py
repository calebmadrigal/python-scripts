# Answer: linkedlist
import re
data = open("p3_data.txt", "r").read().replace("\n", "")
pat = re.compile("[a-z][A-Z]{3}([a-z])[A-Z]{3}[a-z]", re.M)
print ''.join(pat.findall(data))
