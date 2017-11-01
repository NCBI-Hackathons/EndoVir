#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  magicblast_flank_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
from . import magicblast_parser
from . import magicblast_alignment

class MagicblastFlankParser(magicblast_parser.MagicblastParser):

  def __init__(self):
    super().__init__()
    self.extension_reads = {}

  def classify_overlap(self, cols): # qbeg, qend, rbeg, rend, qstrand, rstrand):
    qbeg = int(cols[6])
    qend = int(cols[7])
    rbeg = int(cols[8])
    rend = int(cols[9])
    qlen = int(cols[15])
    rlen = 500
    print(cols[0], cols[1])
    print("Pre q:", qbeg, qend, qlen)
    print("Pre r:", rbeg, rend, qlen)
    if cols[13] == 'minus':    # query is minus, reference is plus
      qbeg, qend = qend, qbeg
    if cols[14] == 'minus':  # Reference is minus , query is plus
      rbeg, rend = rend, rbeg
    print("Post q:", qbeg, qend)
    print("Post r:", rbeg, rend)
     # rhs flank extends to the right
     #  flank:  ..------>
     #  read :       |-------->
    if cols[1].split(':')[1] ==  'rhs':
      if rbeg > rlen-qlen and qend < qlen-10:
        self.alignments.append(magicblast_alignment.MagicblastAlignment(cols))
        print("extend right")
    else:
      # lhs flank extends to the left
      #  flank:       -----...>
      #  read :  |-------->
      #self.check_lhs(qbeg, qend, qlen, cols[13], rbeg, rend, cols[14])
      if rbeg <= 10 and qbeg >= 10:
        self.alignments.append(magicblast_alignment.MagicblastAlignment(cols))
        print("extend left")
    #if self.alignments[-1].qry.name not in self.extension_reads:
      ##self.extension_reads[self.alignments[-1].qry.name] = 0
    #self.extension_reads[self.alignments[-1].qry.name] += 1
    print("==================")

  def parse(self, src):
    self.alignments = []
    read_count = 0
    fh = open("mblast", 'w+')
    for i in src:
      fh.write(i)
      self.classify_overlap(i.strip().split('\t'))
      read_count  += 1
    #for i in self.extension_reads:
      #print(i, self.extension_reads[i])
    print("Init reads:", read_count)
    fh.close()
