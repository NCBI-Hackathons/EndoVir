#  magicblast.py
#
#  Copyright 2017 USYD
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import subprocess
from . import magicblast_parser


class Magicblast:

  def __init__(self):
    self.cmd = 'magicblast'
    self.isPaired = False
    self.num_threads = 2
    self.outfmt = 'tabular'
    self.out = 'magicblast_out'
    self.word_size = 20
    self.perc_identity = 60

  def run(self, db, sra, parser=magicblast_parser.MagicblastParser()):
    magicblast = subprocess.Popen([self.cmd, '-db', db, '-sra', sra,
                                                 '-num_threads', str(self.num_threads),
                                                 '-outfmt', self.outfmt],
                                  stdout=subprocess.PIPE, bufsize=1)
    parser.parse(magicblast.stdout)
    return parser.alignments
