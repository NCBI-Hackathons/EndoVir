#  magicblast_alignment.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


class MagicblastParser:

  def __init__(self):
    self.alignments = []

  def parse(self, src):
    self.alignments = []
    for i in src:
      if i[0] != '#':
        self.alignments.append(lib.alignment.magicblast_alignment.MagicblastAlignment(i.strip().split('\t')))
