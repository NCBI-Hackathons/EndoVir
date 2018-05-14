#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  -------------------------------------------------------------------------------
#  \file megahit.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 2.0.
#  \description
#  -------------------------------------------------------------------------------
import os
import sys



sys.path.insert(1, os.path.join(sys.path[0], '../../src'))

from asm import asm_base

class Megahit(asm_base.AssemblerBaseA):

  def __init__(self):
    super().__init__()
    self.suffix = ".contigs.fa"

  def run(self, reads, prefix=None, outdir='megahit_out'):
    self.parser.reset()
    cmd = [self.path, '--read', reads,
                      '--num-cpu-threads', str(cpu_threads),
                      '--min-contig-len', str(self.min_contig_len),
                      '--keep-tmp-files']
    if prefix == None:
      prefix = reads
    cmd += ['--out-prefix', prefix, '--out-dir', outdir]
    print("Log", cmd)
    megahit = subprocess.call(cmd)
    self.parser.parse(fil=os.path.join(outdir, prefix+self.suffix))
    return os.path.join(outdir, prefix+self.suffix)

  def new(self):
    return Megahit()
