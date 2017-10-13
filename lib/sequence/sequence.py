#  sequence.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

class Sequence:

  def __init__(self, name='', seq=''):
    self.name = name
    self.sequence = seq
    self.length = len(seq)

  def shrink(self, newlen):
    self.sequence = self.seq.substr[:newlen]
    self.length = len(self.seq)

  def subseq(self, start, length, name=None):
    if name == None:
      return Sequence(self.name, self.sequence[start:start+length])
    return Sequence(name, self.sequence[start:start+length])
