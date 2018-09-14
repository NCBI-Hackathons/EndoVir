#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Fasta formatter: formats and return a sequence object as FASTA
#               string.
#-------------------------------------------------------------------------------

class FastaFormatter:

  @staticmethod
  def format(sequence):
    return ">{0}\n{1}\n".format(sequence.name, sequence.sequence)

  @staticmethod
  def format_string(name, sequence):
    return ">{0}\n{1}\n".format(name, sequence)

  def __init__(self):
    pass
