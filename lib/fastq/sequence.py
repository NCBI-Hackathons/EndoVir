#  fastq.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from .. import sequence

class FastqSequence(sequence.sequence.Sequence):

  def __init__(self, name, seq, qual=''):
    super().__init__(name, seq)
    self.qual = qual

  def subseq(self, start, length, name=None):
    if name == None:
      return FastqSequence(self.name, self.sequence[start:start+length], self.qual[start:start+length])
    return FastqSequence(name, self.sequence[start:start+length], self.qual[start:start+length])
