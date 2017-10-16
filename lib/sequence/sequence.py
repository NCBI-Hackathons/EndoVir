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
    self.length = len(seq)
