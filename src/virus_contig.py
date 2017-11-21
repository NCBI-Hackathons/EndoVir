#  contig.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import pathlib

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.magicblast
import lib.process.process
import lib.vdbdump.vdbdump
import lib.sequence.sequence
import lib.fasta.parser

class VirusContig(lib.sequence.sequence.Sequence):

  def __init__(self, name, seq, srr, src, flank_len, screen_dir, flankdb):
    super().__init__(name, seq)
    self.src = src
    self.srr = srr
    self.flankdb = flankdb
    self.flank_len = flank_len
    self.iteration = 0
    self.lhs = None
    self.rhs = None
    self.lhs_extensions = {}
    self.lhs_ext_length = 0
    self.lhs_ext = None
    self.rhs_extensions = {}
    self.rhs_ext_length = 0
    self.rhs_ext = None
    self.wd = os.path.join(screen_dir, self.name)
    if not os.path.exists(self.wd):
      os.mkdir(self.wd)

  def revcomp_seq(self, seq, beg, end):
    revcomp_seq = seq.translate(str.maketrans("ACTG", "TGAC"))
    return revcomp_seq[::-1][beg:end]

  def extend(self):
    #This flank business needs an own class later
    print(self.name)
    ext_alns = []
    if self.lhs_ext != None:
      ext_alns.append(self.lhs_ext)
    if self.rhs_ext != None:
      ext_alns.append(self.rhs_ext)
    vdb = lib.vdbdump.vdbdump.VdbDump()
    reads = vdb.rowids_to_reads(self.srr, ext_alns)
    if self.rhs_ext != None and (self.rhs_ext.qry.sra_rowid in reads):
      print("RHS: Qry", self.rhs_ext.qry.sra_rowid,
                        self.rhs_ext.qry.start,
                        self.rhs_ext.qry.stop,
                        self.rhs_ext.qry.length,
                        self.rhs_ext.qry.strand,
                        "Ref",
                        self.rhs_ext.ref.start,
                        self.rhs_ext.ref.stop,
                        self.rhs_ext.ref.strand)
      if self.rhs_ext.ref.strand == 1 and self.rhs_ext.qry.strand == 0:
        print("RHS: Extending {} as revcomp".format(self.rhs_ext.qry.sra_rowid))
        print(self.revcomp_seq(reads[self.rhs_ext.qry.sra_rowid],
                                      self.rhs_ext.qry.length-self.rhs_ext.qry.start,
                                      self.rhs_ext.qry.length))
        print("Bpoint: contig: {}, read: {}".format(self.name,
                                                    self.rhs_ext.ref.stop+self.rhs_ext.ref.aln_length,
                                                    self.rhs_ext.qry.length-self.rhs_ext.qry.start))
      else:
        print("RHS: Extending {} ".format(self.rhs_ext.qry.sra_rowid))
        print(reads[self.rhs_ext.qry.sra_rowid][self.rhs_ext.qry.stop:])
        print("Bpoint: contig {}: {}, read {}: {}".format(self.name,
                                                          self.rhs_ext.ref.stop,
                                                          self.rhs_ext.qry.sra_rowid,
                                                          self.rhs_ext.qry.stop))

    if self.lhs_ext != None and (self.lhs_ext.qry.sra_rowid in reads):
      print("LHS: Qry: ", self.lhs_ext.qry.sra_rowid,
                          self.lhs_ext.qry.start,
                          self.lhs_ext.qry.stop,
                          self.lhs_ext.qry.length,
                          self.lhs_ext.qry.strand,
                          "Ref",
                          self.lhs_ext.ref.start,
                          self.lhs_ext.ref.stop,
                          self.lhs_ext.ref.strand)
      #if self.rhs_ext.ref.strand == 0 and self.rhs_ext.qry.strand == 1:
       # print("RHS: Extending {} as revcomp".format(self.rhs_ext.qry.sra_rowid))
    print(reads)

  #def update(self, assembly):
    #p = lib.fasta.parser.FastaParser()
    #p.parse(assembly)
    #for i in p.sequences:
      #self.sequence = p.sequences[i].sequence
      #self.length = len(self.sequence)
      #print("Update Iteration {0}:\nContig: {1}\tlen:{2}".format(self.iteration, self.name, self.length))

  #def asses(self, assembly):
    #print("Asses Iteration {0}:\nContig: {1}\tlen:{2}".format(self.iteration, self.name, self.length))
    #self.update(assembly)
