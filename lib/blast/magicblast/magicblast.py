#  magicblast.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import subprocess

sys.path.insert(1, os.path.join(sys.path[0], '../../'))
import lib.vdbdump.vdbdump
from . import magicblast_parser


class Magicblast:

  def __init__(self, path='magicblast'):
    self.path = path
    self.isPaired = False
    self.num_threads = 2
    self.outfmt = 'tabular'
    self.out = 'magicblast_out'
    self.word_size = 20
    self.perc_identity = 60
    self.vdbdump = lib.vdbdump.vdbdump.VdbDump()
    self.parser = magicblast_parser.MagicblastParser()

  def run(self, srr, db):
    cmd = [self.path, '-db', db, '-sra', srr,'-num_threads', str(self.num_threads),
                                              '-outfmt', self.outfmt]
    print(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
    self.parser.parse(p.stdout)
    self.vdbdump.run(srr, self.parser.alignments)

  # Unfortunately, databasea re still required when using several threads
  #def run_subject_file(self, srr, fil):
    #cmd = [self.path, '-subject', fil, '-sra', srr,'-num_threads', str(self.num_threads),
                                                        #'-outfmt', self.outfmt]
    #print(cmd)
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
    #self.parser.parse(p.stdout)
    #self.vdbdump.run(srr, self.parser.alignments)
