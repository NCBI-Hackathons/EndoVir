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
    self.results = None

  def identify_overlaps(self, cols, contigs):
    qbeg = int(cols[6])
    qend = int(cols[7])
    rbeg = int(cols[8])
    rend = int(cols[9])
    qlen = int(cols[15])
    if cols[13] == 'minus':    # query is minus (rt), reference is plus
      qbeg, qend = qend, qbeg
    if cols[14] == 'minus':  # Reference is minus (rt) , query is plus
      rbeg, rend = rend, rbeg
    cnt = cols[1].split(':')[0]
    if cnt in contigs:
      if contigs[cnt].rhs == None:
        if rbeg > 10 and rend < self.flank_len - 10:
          pass # skip nested read mappings
        else:
          a = magicblast_alignment.MagicblastAlignment(cols)
          contigs[cnt].lhs_extensions[a.sra_rowid] = 0
          self.alignments.append(a)
      else:
        if cols[1].split(':')[1] ==  'rhs':
          if rbeg > contigs[cnt].flank_len - qlen and qend < qlen-10:
            a = magicblast_alignment.MagicblastAlignment(cols)
            a.isRhsFlank = True
            if rbeg + qlen > contigs[cnt].rhs_ext_length:
              contigs[cnt].rhs_ext_length = rbeg + qlen
              contigs[cnt].rhs_ext = a
            contigs[cnt].rhs_extensions[a.qry.sra_rowid]= 0
            self.alignments.append(a)
            #print("extend right")
        else:
          if rbeg <= 10 and qbeg >= 10:
            a = magicblast_alignment.MagicblastAlignment(cols)
            a.isLhsFlank = True
            if rbeg + qlen > contigs[cnt].lhs_ext_length:
              contigs[cnt].lhs_ext_length = rbeg + qlen
              contigs[cnt].lhs_ext = a
            contigs[cnt].lhs_extensions[a.qry.sra_rowid] = 0
            self.alignments.append(a)
            #print("extend right")
      #print("======================")


  def parse(self, src, contigs):
    self.alignments = []
    read_count = 0
    for i in src:
      print(i)
      self.identify_overlaps(i.strip().split('\t'), contigs)
      read_count  += 1
    print("Overlapping reads: {}/{}".format(len(self.alignments), read_count))
    return self.alignments
