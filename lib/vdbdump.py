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

from . import sequence

class VdbDump:

  def __init__(self):
    self.cmd = 'vdb-dump'
    self.format = 'fastq'
    self.batch_size = 10000

  def run(self, srr, alignments=None):
    opts = [self.cmd, '--format', self.format]
    sequences = []

    aln_idx = 0
    for i in range(0, len(alignments), self.batch_size):
      cmd = opts + ['-R', ','.join(str(x.sra_rowid) for x in alignments[i:i+self.batch_size]), srr]
      vd = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
      line_count = 1
      header = ''
      seq = ''
      qual = ''
      for i in vd.stdout:
        #print(i.strip().decode())
        if line_count == 1:
          header = i.strip().decode()[1:]
        if line_count == 2:
          #seq = i.strip().decode()[alignments[len(sequences)].pos:alignments[len(sequences)].pos+alignments[len(sequences)].length]
          seq = i.strip().decode()
          print(alignments[len(sequences)].pos, "->", alignments[len(sequences)].pos+alignments[len(sequences)].length)
          print(seq)
        if line_count == 4:
          sequences.append(sequence.FastqSequence(header, seq))
          qual = i.strip().decode()
          if len(qual) > 0:
            sequences[-1].qual = qual[alignments[len(sequences)].pos:alignments[len(sequences)].pos+alignments[len(sequences)].length]
          line_count = 0
        line_count += 1
    for i in sequences:
      print(i.name, i.sequence, i.qual)
    print(srr, len(alignments))
    print(len(sequences))
