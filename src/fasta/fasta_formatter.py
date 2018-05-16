#-------------------------------------------------------------------------------
#  \file fasta_formatter.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description Fasta formatter: formats and return a sequence object as FASTA
#               string.
#-------------------------------------------------------------------------------

class FastaFormatter:

  @staticmethod
  def reformat(self, sequence):
    return ">{0}\n{1}\n".format(sequence.name, sequence.sequence)

  def __init__(self):
    pass
