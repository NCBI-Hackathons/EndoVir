#  rpstblastn.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import subprocess

class RpstBlastn:

  def __init__(self):
    self.path = 'rpstblastn'
    #self.outfmt = "7 qseqid qlen sseqid slen sscinames evalue bitscore score length pident nident mismatch positive gapopen gaps ppos qframe sframe sstrand qcovs qcovhsp qstart qend sstart send qseq sseq"
    self.outfmt = 15
    self.max_eval = 0.001

  def run(self, query, db, outf='rpst_out'):
    cmd = [self.path, '-query', query,
                      '-db', db,
                      '-out', outf,
                      '-evalue', str(self.max_eval),
                      '-outfmt', str(self.outfmt)]
    print("Log", cmd)
    blast = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print(blast.stdout)
