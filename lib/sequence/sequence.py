#  sequence.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

class Sequence:

  def __init__(self, name=None, seq=None):
    self.name = name
    self.sequence = seq
    self.length = 0 if seq == None else len(seq)

  def subseq(self, start, length, name=None):
    return self.sequence[start:start+length]
