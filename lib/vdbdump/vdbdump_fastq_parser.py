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

  def parse(self, vdb_out, alignments, fh_flanks):
    line_count = 1
    header = ''
    seq = ''
    qual = ''
    row_idx = 1
    for i in vdb_out:
      if line_count == 1:
        headerline = i.strip().decode()[1:]
        header = headerline.split(' ')[0]
      if line_count == 2:
        seq = i.strip().decode()[alignments[row_idx].qry.start:alignments[row_idx].qry.start+alignments[row_idx].qry.length+1]
      if line_count == 4:
        qual = i.strip().decode()
        if len(qual) > 0:
          qual = qual[alignments[row_idx].qry.start:alignments[row_idx].qry.start+alignments[row_idx].qry.length+1]
        else:
          qual = len(seq) * self.qual_placeholder
        s = sequence.FastqSequence(header, seq, qual)
        row_idx += 1
        fh_flanks.write(s.get_sequence())
        #self.sequences.append()
        line_count = 0
      line_count += 1
