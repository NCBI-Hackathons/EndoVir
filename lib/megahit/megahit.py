#  megahit.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import subprocess

class Megahit:

  def __init__(self):
    self.cmd = 'megahit'
    self.num_cpu_threads = 2
    self.out_prefix = ''
    self.out_dir = 'megahit_out'

  def run(self, reads):
    megahit = subprocess.call([self.cmd, '--read', reads,
                                          '--out-prefix', self.out_prefix,
                                          '--out-dir', self.out_dir])
