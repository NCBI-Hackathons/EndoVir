#  rpstblastn.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import subprocess

def RpstBlastn:

  def __init__(self):
    self.cmd = 'rpstblastn'
    self.db  = 'cdd'
    self.out = 'rpst_out'
    self.gilist = 'cdd.virus.accs'
    self.outfmt = -outfmt "7 qseqid qlen sseqid slen sscinames evalue bitscore score length pident nident mismatch positive gapopen gaps ppos qframe sframe sstrand qcovs qcovhsp qstart qend sstart send qseq sseq"

  def run(self, query):
    blast = subprocess.Popen([self.cmd, '-query', query,
                                        '-db', self.db,
                                        '-gilist', self.gilist],
                             stdout=subprocess.PIPE)
