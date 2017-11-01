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

  def run(self, srr, alignments, parser=vdbdump_fastq_parser.VdbdumpFastqParser()):
    opts = [self.cmd, '--format', self.format]
    print("Reads to dump:", len(alignments))
    batch_size = self.batch_size
    for i in range(0, len(alignments), batch_size):
      print("In geenrator:", len([x.qry.sra_rowid for x in alignments[i:i+self.batch_size]]))
      cmd = opts + ['-R', ','.join(str(x.qry.sra_rowid) for x in alignments[i:i+self.batch_size]), srr]
      print(cmd)
      vd = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
      parser.parse(vd.stdout, alignments[i:i+batch_size])
    return parser
