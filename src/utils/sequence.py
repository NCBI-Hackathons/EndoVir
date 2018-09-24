#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Implementation of a biological sequence.
#-------------------------------------------------------------------------------

class Sequence:

  def __init__(self, name=None, sequence=None, metadata=None):
    self.name = name
    self.sequence = sequence
    self.length = 0
    if sequence != None:
      self.length = len(sequence)
    self.metadata = metadata

  def format(self, formatter):
    return formatter.format(self)
