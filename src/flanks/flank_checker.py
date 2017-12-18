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

    def __init__(self, l_from, l_to, l_strand, r_from, r_to, r_strand):
      self.lhs_from = l_from
      self.lhs_to = l_to
      self.lhs_strand = l_strand
      self.rhs_from = r_from
      self.rhs_to= r_to
      self.rhs_strand = r_strand

  def __init__(self):
    super().__init__()
    self.updates = {}

  def check(self, contigs, lnk):
    for i in self.hspmap:
      flankA = lnk.get_flank(self.hspmap[i].query.title)
      flankB = lnk.get_flank(self.hspmap[i].hit.accession)
      if flankA.contig.name != flankB.contig.name:
        print(flankA.contig.name, flankA.name, flankB.contig.name, flankB.name)
        print("\t", self.hspmap[i].query.title, self.hspmap[i].query_from,
                    self.hspmap[i].query_to,    self.hspmap[i].query_strand,
                    self.hspmap[i].qseq)
        print("\t", self.hspmap[i].hit.accession, self.hspmap[i].hit_from,
                    self.hspmap[i].hit_to, self.hspmap[i].hit_strand,
                    self.hspmap[i].hseq)
        if flankA.side == 'rhs' and flankB.side == 'lhs':
          print("{}:{} + {}:{}".format(flankA.contig.name, flankA.side, flankB.contig.name, flankB.side))
          c = self.ContigOverlap(self.hspmap[i].query_from, self.hspmap[i].query_to,
                                 self.hspmap[i].query_strand, self.hspmap[i].hit_from,
                                 self.hspmap[i].hit_to, self.hspmap[i].hit_strand)
          flankA.contig.merge_contig_rhs(flankA, flankB.contig, c)
        elif flankA.side == 'lhs' and flankB.side == 'rhs':
          pass
          #flankB.contig.merge_contig_rhs(flankA, c)
        else:
          print("One flank is on the other strand")
      else:
        if flankA.name != flankB.name:
          raise NotImplementedError("Smells like circular or terminal repeat business. \
                                    Not yet implemented. How about now?")


  def update(self):
    if self.hspmap[i].query.title in self.updates:
      c = self.ContigOverlap()
