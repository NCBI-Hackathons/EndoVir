#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  magicblast_flank_parser.py
#
#  Copyright 2017 USYD
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

  def classify_overlap(self, cols): # qbeg, qend, rbeg, rend, qstrand, rstrand):
    qbeg = int(cols[6])
    qend = int(cols[7])
    rbeg = int(cols[8])
    rend = int(cols[9])
    qlen = 500
    #print(cols[0], cols[1])
    #print("Pre q:", qbeg, qend)
    #print("Pre r:", rbeg, rend)
    if cols[13] == 'minus':    # query is minus, reference is plus
      qbeg, qend = qend, qbeg
    if cols[14] == 'minus':  # Reference is minus , query is plus
      rbeg, rend = rend, rbeg
    #print("Post q:", qbeg, qend)
    #print("Post r:", rbeg, rend)
     # rhs flank extends to the right
     #  flank:  ..------>
     #  read :       |-------->
    if cols[1].split(':')[1] == 'rhs':
      if rbeg + int(cols[15]) > qlen:
        self.alignments.append(magicblast_alignment.MagicblastAlignment(cols))
        #print("extend right")
    else:
      # lhs flank extends to the left
      #  flank:       -----...>
      #  read :  |-------->
      if rbeg + int(cols[15]) < qlen:
        self.alignments.append(magicblast_alignment.MagicblastAlignment(cols))
        #print("extend left")
    #print("==================")

  def parse(self, src):
    self.alignments = []
    read_count = 0
    for i in src:
      self.classify_overlap(i.strip().split('\t'))
      read_count  += 1
    print("Init reads:", read_count)
