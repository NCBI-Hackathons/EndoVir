#  rpstblastn.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import subprocess

from .. parser import blast_json

class RpstBlastn:

  def __init__(self):
    self.path = 'rpstblastn'
    self.outfmt = 15
    self.max_eval = 0.001
    self.parser = blast_json.BlastParser()

  def run(self, query, db, outf='rpst_out'):
    cmd = [self.path, '-query', query,
                      '-db', db,
                      '-evalue', str(self.max_eval),
                      '-outfmt', str(self.outfmt)]
    print("Log", cmd)
    self.parser.reset()
    blast = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    self.parser.parse(blast.stdout)
    if len(self.parser.querymap) > 0:
      return [self.parser.querymap[x].title for x in self.parser.querymap]
    return []
