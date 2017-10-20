# -*- coding: utf-8 -*-
#
#  vdbdump.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import json
import subprocess

from . import vdbdump_fastq_parser

class VdbDump:

  def __init__(self):
    self.cmd = 'vdb-dump'
    self.format = 'fastq'
    self.batch_size = 10000
    self.parser = vdbdump_fastq_parser.VdbdumpFastqParser()

  def run(self, srr, alignments):
    opts = [self.cmd, '--format', self.format]
    for i in range(0, len(alignments), self.batch_size):
      cmd = opts + ['-R', ','.join(str(x.sra_rowid) for x in alignments[i:i+self.batch_size]), srr]
      vd = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
      self.parser.parse(vd.stdout, alignments)
