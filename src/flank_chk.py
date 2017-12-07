#  flank_checker.py
#
#  Copyright 2017 USYD
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import io
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.parser.blast_json

class FlankChecker(lib.blast.parser.blast_json.BlastParser):

  class ContigOverlap:

    def __init__(self):
      self.lhs = None
      self.lhs_start = 0
      self.lhs_stop = 0
      self.lhs_strand = 0

      self.rhs = None
      self.rhs_start = 0
      self.rhs_stop= 0
      self.rhs_strand = 0

  def __init__(self):
    super().__init__()
    self.updates = {}

  def check(self, contigs, lnk):
    for i in self.hspmap:
      flkA = lnk.get_flank(self.hspmap[i].query.title)
      flkB = lnk.get_flank(self.hspmap[i].hit.accession)
      if flkA.name != flkB.name:
        print(i, self.hspmap[i].score, self.hspmap[i].alength, self.hspmap[i].identity)
        print("\t", self.hspmap[i].query.title,
                    self.hspmap[i].query_from,
                    self.hspmap[i].query_to,
                    self.hspmap[i].query_strand,
                    self.hspmap[i].qseq)
        print("\t", self.hspmap[i].hit.accession,
                    self.hspmap[i].hit_from,
                    self.hspmap[i].hit_to,
                    self.hspmap[i].hit_strand,
                    self.hspmap[i].hseq)
        if self.hspmap[i].query_strand == self.hspmap[i].hit_strand:
          if flkA.side == 'rhs':
            c = self.ContigOverlap()
            c.lhs_start = self.hspmap[i].query_from
            c.lhs_stop  = self.hspmap[i].query_to
            c.rhs_start = self.hspmap[i].hit_from
            c.rhs_stop  = self.hspmap[i].hit_to
            flkA.contig.anneal_rhs(flkB, c)
          #if flkA.side == 'lhs':
            #flkA.contig.anneal_lhs(flkB.contig, c)

  def update(self):
    if self.hspmap[i].query.title in self.updates:
      c = self.ContigOverlap()
