#  magicblast_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#  https://ncbi.github.io/magicblast/doc/output.html
#  Version: 0.0


from .import magicblast_alignment

class MagicblastParser:

  def __init__(self):
    self.alignments = []

  def parse(self, src):
    self.alignments = []
    for i in src:
      if i[0] != '#':
        self.alignments.append(magicblast_alignment.MagicblastAlignment(i.strip().split('\t')))
