# -*- coding: utf-8 -*-
#
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
    self.out_prefix = None
    self.out_dir = 'megahit'
    self.word_size = 20
    self.perc_identity = 60

  def run(self, fin)
    megahit -r $input_file --out-prefix $output_file --out-dir $dir_name

    megahit = subprocess.Popen([self.cmd, '-db', db, '-sra', sra,
                                             '-num_threads', str(self.num_threads),
                                             '-outfmt', self.outfmt],
                                  stdout=subprocess.PIPE, bufsize=1)
    parser.parse(magicblast.stdout)
