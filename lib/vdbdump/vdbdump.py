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
    print("Reads to dump:", len(alignments), file=sys.stderr)
    batch_size = self.batch_size
    parser.reset()
    for i in range(0, len(alignments), batch_size):
      cmd = opts + ['-R', ','.join(str(x.qry.sra_rowid) for x in alignments[i:i+self.batch_size]), srr]
      print(cmd)
      vd = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
      parser.parse(vd.stdout, alignments[i:i+batch_size])
    return parser

  def dump_to_stream(self, srr, alignments, stream, fmt='fasta'):
    opts = [self.cmd, '--format', fmt]
    batch_size = self.batch_size
    for i in range(0, len(alignments), batch_size):
      cmd = opts + ['-R', ','.join(str(x.qry.sra_rowid) for x in alignments[i:i+self.batch_size]), srr]
      print(cmd)
      vd = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
      stream.write(vd.stdout.read().decode())

  def rowids_to_reads(self, srr, alignments):
    opts = [self.cmd, '--format', 'tab', '-C', 'NAME,READ']
    batch_size = self.batch_size
    reads = {}
    for i in range(0, len(alignments), batch_size):
      cmd = opts + ['-R', ','.join(str(x.qry.sra_rowid) for x in alignments[i:i+self.batch_size]), srr]
      print(cmd)
      vd = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
      for i in vd.stdout:
        fields = i.strip().split('\t')
        reads[fields[0]] = fields[1]
    return reads
