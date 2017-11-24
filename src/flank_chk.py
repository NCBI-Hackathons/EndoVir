#  flank_checker.py
#
#  Copyright 2017 USYD
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import io
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.parser.blast_json

class FlankChecker(lib.blast.parser.blast_json.BlastParser):

  def __init__(self):
    super().__init__()

  def check(self, contigs):
    print(contigs)
    for i in self.hitmap:
      print(i, self.hitmap[i].accession)
    for i in self.hspmap:
      print(i, self.hspmap[i].query.title, self.hspmap[i].hit.accession)
