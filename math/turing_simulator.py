#!/usr/bin/env python
#
# AUTHOR
#    Caleb Madrigal
#
# DESCRIPTION
#    A basic turing machine simulator which runs through the programmed rules on the given initial tape.
#    Usage: python turing_simulator.py

import time

HALT = 999
position_map = {'L': -1, 'R': 1}

class TuringPartialFunction:
   def __init__(self, trans_rules):
      # Make dictionary mapping from (state, value) to (new_state, new_value, R) for each rule: (s, v, ns, nv, R)
      self.rules = dict(map(lambda x: (x[0:2], x[2:]), trans_rules))

   def execute(self, state, cell):
      if (state, cell) in self.rules:
         return self.rules[(state, cell)]
      else:
         return (HALT, HALT, HALT)

class TuringTape:
   def __init__(self, tape_str):
      self.position = 0
      self.left_bound = 0
      self.right_bound = len(tape_str)
      self.tape = [item for item in tape_str]
   def getcell(self, index):
      if index < self.left_bound:
         self.left_bound = self.left_bound - 1
         self.tape.insert(0, 'B')
      elif index >= self.right_bound:
         self.right_bound = self.right_bound + 1
         self.tape.append('B')
      self.position = index
      return self.tape[self.position - self.left_bound]
   def setcell(self, index, value):
      self.tape[index] = value
   def __str__(self):
      return ''.join(self.tape)
   def __repr__(self):
      return ''.join(self.tape)

class TuringMachine:
   def __init__(self, part_func, tape):
      self.part_func = part_func
      self.tape = tape
      self.position = 0
      self.state = 's0'

   def step(self):
      (new_state, new_cell, direction) = self.part_func.execute(self.state, self.tape[self.position])

      if new_cell == new_state == direction == HALT:
         return HALT

      self.tape[self.position] = new_cell
      self.state = new_state
      self.position = self.position + position_map[direction]
      # TODO: When position is out of bounds, extend tape

   def __str__(self):
      #return "Tape = %r\nPosition = %s\nState = %s\n" % (self.tape, self.position, self.state)
      tape = ''.join(self.tape)
      control_head = '^'.rjust(self.position+1)
      state = self.state.rjust(self.position+1)
      return tape + '\n' + control_head + '\n' + state + '\n\n'

def main():
   trans_rules = [('s0', '1', 's1', 'B', 'R'),
                  ('s1', '*', 's3', 'B', 'R'),
                  ('s1', '1', 's2', 'B', 'R'),
                  ('s2', '1', 's2', '1', 'R'),
                  ('s2', '*', 's3', '1', 'R')]

   part_func = TuringPartialFunction(trans_rules)

   tape_str = "111111111*111111B" # 8+5
   tape = [item for item in tape_str]

   t = TuringMachine(part_func, tape)

   while 1:
      time.sleep(1)
      retval = t.step()
      print t
      if retval == HALT:
         print "Turing Machine HALTED."
         break

if __name__ == "__main__":
   main()
