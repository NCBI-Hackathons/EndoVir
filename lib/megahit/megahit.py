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

#sys.path.insert(1, os.path.join(sys.path[0], '../../src'))
from process import basic_process

class Megahit(basic_process.BasicProcess):

  def __init__(self):
    super().__init__()
    self.suffix = ".contigs.fa"

  def get_output(self):
    return os.path.join(self.option_map['--out-dir'],
                        self.option_map['--prefix']+self.suffix)
  #def run(self, reads, 'megahit_out'):
    #self.options
    #cmd = [self.path, '--read', reads,
                      #'--num-cpu-threads', str(cpu_threads),
                      #'--min-contig-len', str(self.min_contig_len),
                      #'--keep-tmp-files']
    #if prefix == None:
      #prefix = reads
    #cmd += ['--out-prefix', prefix, '--out-dir', outdir]
    #print("Log", cmd)
    #megahit = subprocess.call(cmd)
    #self.parser.parse(fil=os.path.join(outdir, prefix+self.suffix))
    #return os.path.join(outdir, prefix+self.suffix)

  #def new(self):
    #return Megahit()
