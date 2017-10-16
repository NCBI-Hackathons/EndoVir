#  fasta.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


from ..sequence import sequence

class FastaSequence(sequence.Sequence):

  def __init__(self, name, seq):
    super().__init__(name, seq)
    self.header = name
    self.name = name.split(' ')[0]


  def get_sequence(self):
    return ">{0}\n{1}\n".format(self.header, self.sequence)

  def subseq(self, start, length, header=None):
    if header == None:
      return FastaSequence(self.header, self.sequence[start:start+length])
    return FastaSequence(header, self.sequence[start:start+length])
