# Implementation of Rule 110 (http://en.wikipedia.org/wiki/Rule_110), a cellular automaton.
# Author: Caleb Madrigal

import time

class CircularList(list):
   def __getitem__(self, key):
      return list.__getitem__(self, key % len(self))

def rule110(s):
   if s[1] == "0" and s[2] == "1": return "1"
   elif s[0] == s[1] == s[2] == "1": return "0"
   else: return s[1]

def run110(initial_state):
   new_state = CircularList(initial_state)
   while 1:
      state = CircularList(new_state)
      for i in range(len(state)):
         pattern = state[i-1]+state[i]+state[i+1]
         new_state[i] = rule110(pattern)
      yield state

def pretty(lst):
   return ''.join(lst).replace('0',' ').replace('1','#')

if __name__ == "__main__":
   try:
      items = ["0" for i in range(99)] + ["1"]
      g = run110(items)
      for i in range(10000):
         print pretty(g.next())
         time.sleep(.25)
   except KeyboardInterrupt:
      pass
