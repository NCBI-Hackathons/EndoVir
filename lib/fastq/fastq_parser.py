#  fastq_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from ..sequence import sequence

class FastqParser:

  def __init__(self):
    self.sequences = []

  def parse(self, src):
    line_count = 1
    header = ''
    seq = ''
    qual = ''
    for i in src:
      if line_count == 1:
        header = i.strip()[1:]
      if line_count == 2:
        seq = i.strip()
      if line_count == 4:
        sequences.append(sequence.FastqSequence(header, seq))
        qual = i.strip().decode()
        line_count = 0
      line_count += 1
