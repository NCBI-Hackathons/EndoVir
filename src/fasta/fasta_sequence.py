#-------------------------------------------------------------------------------
#  \file fasta_sequence.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description Fasta sequecne implementation. Inherits Sequence().
#-------------------------------------------------------------------------------


from ..sequence import sequence

class FastaSequence(sequence.Sequence):

  def __init__(self, name=None, seq=None):
    super().__init__(name, seq)

  def get_sequence(self):
    return ">{0}\n{1}\n".format(self.name, self.sequence)
