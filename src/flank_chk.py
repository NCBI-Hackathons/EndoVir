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

  class FlankOverlap:

    def __init__(self):
      self.lhs = None
      self.lhs_start = 0
      self.lhs_stop = 0

      self.rhs = None
      self.rhs_start = 0
      self.rhs_stop= 0

  def __init__(self):
    super().__init__()
    self.checked = {}

  def check(self, contigs):
    print(contigs)
    for i in self.hspmap:
      if  self.hspmap[i].query.title[:5] != self.hspmap[i].hit.accession[:5]:
        print(i, self.hspmap[i].score,
                 self.hspmap[i].alength,
                 self.hspmap[i].identity)
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
        #qry_ctg, qry_ext = self.hspmap[i].query.title.split(':')
        #qry_loc = qry_ext.split("_")[0]
        #hit_ctg, hit_loc = self.hspmap[i].hit.accession.split(':')
        #if self.hspmap[i].query_strand != self.hspmap[i].hit_strand:
          #raise NotImplementedError("Simple diff ori not implemented. Check alignment")
        #elif self.hspmap[i].alength >= contigs[qry_ctg].flank_len:
          #raise NotImplementedError("Repeat analysis not implemneted. Overlap longer than flank len.")
        #elif qry_loc == hit_loc:
          #raise NotImplementedError("Posiblle diff ori not implemented. Same flank from two contigs overlap.")
        #elif qry_loc != hit_loc:
          #if contigs[qry_ctg].lhs_ext == None:
            #contigs[qry_ctg].extend_rhs(self.hspmap[i].query_to, contigs[hit_ctg], self.hspmap[i].hit_to)
          #elif contigs[qry_ctg].rhs_ext == None:
            #contigs[hit_ctg].extend_rhs(self.hspmap[i].hit_to, contigs[qry_ctg], self.hspmap[i].query_to)
          #else:
            #contigs[qry_ctg].extend_rhs(self.hspmap[i].query_to, contigs[hit_ctg], self.hspmap[i].hit_to)
        #else:
          #print(contigs[qry_ctg].name, qry_loc,  contigs[qry_ctg].name, hit_loc)
          #raise NotImplementedError("Non-envisioned case.")
        #print("------")

    def update_contig_list(self):
      pass
