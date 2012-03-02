# Answer: 5808 (Needed to look up answer).

#a =  [1, 11, 21, 1211, 111221]
#len   1  2   2   4     6
#sum   1  2   3   5     8 (fibonacci [minus f0])
#index 0  1   2   3     4

#f0 = 2
#f1 = 2
#f = [f0, f1]
#def fib(f_minus_1, f_minus_2):
#   return f_minus_1 + f_minus_2
#
#for i in range(35):
#   f.append(fib(f[-1], f[-2]))
#
#for i in range(35):
#   print "fib[%d] = %d" % (i, f[i])

a=['1']
for i in range(30):
    elem=a[-1]+'?'
    next=[]
    start=0
    for end in range(len(elem)):
        if elem[end]!=elem[start]:
            next.append(str(end-start)+elem[start])
            start=end
    a.append("".join(next))
print len(a[-1])
