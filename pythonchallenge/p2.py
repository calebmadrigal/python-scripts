# Answer: equality
data = open("p2_data.txt").read()
char_order = []
char_count = {}
answer = ""

for c in data:
   if char_count.has_key(c):
      char_count[c] += 1
   else:
      char_order.append(c)
      char_count[c] = 1

for c in char_order:
   if char_count[c] == 1:
      answer += c

print answer
