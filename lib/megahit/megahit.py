#  megahit.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import subprocess

class Megahit:

  def __init__(self, path='megahit'):
    self.path = path
    self.suffix = ".contigs.fa"
    self.min_contig_len = 400

  def run(self, reads, prefix=None, outdir=None, cpu_threads=2):
    cmd = [self.path, '--read', reads,
                      '--num-cpu-threads', str(cpu_threads),
                      '--min-contig-len', str(self.min_contig_len)]
    if prefix != None:
      cmd += ['--out-prefix', prefix]
    if outdir != None:
      cmd += ['--out-dir', outdir]
    print("Log", cmd)
    megahit = subprocess.call(cmd)
    return os.path.join(outdir, prefix+self.suffix)
