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
        qry_ctg, qry_ext = self.hspmap[i].query.title.split(':')
        qry_loc = qry_ext.split("_")[0]
        hit_ctg, hit_loc = self.hspmap[i].hit.accession.split(':')
        if self.hspmap[i].query_strand != self.hspmap[i].hit_strand:
          raise NotImplementedError("Simple diff ori not implemented. Check alignment")
        elif self.hspmap[i].alength >= contigs[qry_ctg].flank_len:
          raise NotImplementedError("Repeat analysis not implemneted. Overlap longer than flank len.")
        elif qry_loc == hit_loc:
          raise NotImplementedError("Posiblle diff ori not implemented. Same flank from two contigs overlap.")
        else:
          if qry_loc == 'rhs':
            self.merge_rhs(contigs[qry_ctg], self.hspmap[i].query_to,
                           contigs[hit_ctg], self.hspmap[i].hit_from)
          else:
            self.merge_lhs(contigs[qry_ctg], self.hspmap[i].query_to,
                           contigs[hit_ctg], self.hspmap[i].hit_from)
#          contigs[qry_ctg].update_rhs(contigs[hit_ctg], )
        print("------")

  def merge_rhs(self, qry, qry_break, hit, hit_break):
    rhs_ext = qry.rhs_ext_seq.sequence[:qry_break] + hit.sequence[hit_break:]
    print(rhs_ext)

  def merge_lhs(self, qry, qry_break, hit, hit_break):
    lhs_ext = qry.rhs_ext_seq.sequence[:qry_break] + hit.sequence[hit_break:]
    print(rhs_ext)

  def update_rhs(self, ctg):
    pass
