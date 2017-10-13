#  fastq_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from ..fastq import fastq_parser
from ..fastq import sequence
class VdbdumpFastqParser(fastq_parser.FastqParser):

  def __init__(self):
    super().__init__()
    self.qual_placeholder = '$'

  def parse(self, vdb_out, alignments):
    line_count = 1
    header = ''
    seq = ''
    qual = ''
    for i in vdb_out:
      if line_count == 1:
        header = i.strip().decode()[1:]
      if line_count == 2:
        seq = i.strip().decode()[alignments[len(self.sequences)].qry.start:alignments[len(self.sequences)].qry.start+alignments[len(self.sequences)].qry.length+1]
      if line_count == 4:
        qual = i.strip().decode()
        if len(qual) > 0:
          qual = qual[alignments[len(self.sequences)].qry.start:alignments[len(self.sequences)].qry.start+alignments[len(self.sequences)].qry.length+1]
        else:
          qual = len(seq) * self.qual_placeholder
        self.sequences.append(sequence.FastqSequence(header, seq, qual))
        line_count = 0
      line_count += 1
