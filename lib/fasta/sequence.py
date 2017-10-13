#  fasta.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


from ..sequence import sequence

class FastaSequence(sequence.Sequence):

  def __init__(self, name='', seq=''):
    super().__init__()
    self.header = name

  def get_sequence(self):
    return ">{0}\n{1}".format(self.header, self.name)

  def subseq(self, start, length, header=None):
    if header == None:
      return FastaSequence(self.header, self.sequence[start:start+length])
    return FastaSequence(header, self.sequence[start:start+length])
