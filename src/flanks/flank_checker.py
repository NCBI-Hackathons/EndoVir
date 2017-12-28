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

  def __init__(self):
    super().__init__()
    self.updates = {}

  def check(self, contigs, lnk):
    for i in self.hspmap:
      flankA = lnk.get_flank(self.hspmap[i].query.title)
      flankB = lnk.get_flank(self.hspmap[i].hit.accession)
      if flankA.contig.name != flankB.contig.name:
        print("Put. merge", flankA.contig.name, flankA.name, flankB.contig.name, flankB.name)
        #print("\t", self.hspmap[i].query.title, self.hspmap[i].query_from,
                    #self.hspmap[i].query_to,    self.hspmap[i].query_strand,
                    #self.hspmap[i].qseq)
        #print("\t", self.hspmap[i].hit.accession, self.hspmap[i].hit_from,
                    #self.hspmap[i].hit_to, self.hspmap[i].hit_strand,
                    #self.hspmap[i].hseq)
        if flankA.name in self.updates:
          print("{} is now {}".format(flankA.name, self.updates[flankA.name].name))
          flankA = self.updates[flankA.name]
        if flankB.name in self.updates:
          print("{} is now {}".format(flankB.name, self.updates[flankB.name].name))
          flankB = self.updates[flankB.name]
        if flankA.contig.name == flankB.contig.name:
          continue
        if flankA.side == 'rhs' and flankB.side == 'lhs':
          print("{}:{} + {}:{}".format(flankA.contig.name, flankA.side, flankB.contig.name, flankB.side))
          flankA.contig.merge_contig_rhs(flankB.contig)
          self.update_flank_map(contigs, flankA, flankB)
        elif flankA.side == 'lhs' and flankB.side == 'rhs':
          print("{}:{} + {}:{}".format(flankB.contig.name, flankB.side, flankA.contig.name, flankA.side))
          flankB.contig.merge_contig_rhs(flankA.contig)
          self.update_flank_map(contigs, flankB, flankA)
        else:
          print("One flank is on the other strand")
      else:
        print(flankA.contig.name, flankA.name, flankB.contig.name, flankB.name)
        if flankA.name != flankB.name:
          raise NotImplementedError("Smells like circular or terminal repeat business. \
                                    Not yet implemented. How about now?")
  def update_flank_map(self, contigs, anchor_flank, merged_flank):
    print("---------------------------")
    print("Anchor: {}\tMerge: {}".format(anchor_flank.contig.name, merged_flank.contig.name))
    addFlanks = True
    for i in self.updates:
      if self.updates[i].name == merged_flank.name:
        self.updates[i].contig.lhs_flank = anchor_flank.contig.lhs_flank
        self.updates[i].contig.rhs_flank = anchor_flank.contig.rhs_flank
        addFlank = False
        break
    if addFlanks:
      print(merged_flank.contig.name, anchor_flank.contig.name)
      self.updates[merged_flank.contig.lhs_flank.name] = anchor_flank.contig.lhs_flank
      self.updates[merged_flank.contig.rhs_flank.name] = anchor_flank.contig.rhs_flank
    print(contigs)
    if merged_flank.contig.name in contigs:
      print("rm: ", merged_flank.contig.name)
      del contigs[merged_flank.contig.name]
