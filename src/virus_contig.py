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
    self.lhs_ext_seq = None
    self.rhs_ext_seq = None
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

  def extend(self, stdout):
    #This flank business needs an own class later
    print("Ext\tContig\tFlank\tBpoint_F\tRead\tBpoint_R\tisRevComp\tgrow\tseq")
    ext_alns = []
    if self.lhs_ext != None:
      ext_alns.append(self.lhs_ext)
    if self.rhs_ext != None:
      ext_alns.append(self.rhs_ext)
    vdb = lib.vdbdump.vdbdump.VdbDump()
    reads = vdb.rowids_to_reads(self.srr, ext_alns)

    if self.rhs_ext != None and (self.rhs_ext.qry.sra_rowid in reads):
      isRevComp = False
      extseq = ''
      bpoint_f = 0
      bpoint_r = 0
      if self.rhs_ext.ref.strand == 1 and self.rhs_ext.qry.strand == 0:
        isRevComp = True
        extseq = self.revcomp_seq(reads[self.rhs_ext.qry.sra_rowid],
                                  self.rhs_ext.qry.length-self.rhs_ext.qry.start+1,
                                  self.rhs_ext.qry.length)
        stdout.write(self.anneal_extension('rhs', self.revcomp_seq(reads[self.rhs_ext.qry.sra_rowid],
                                     self.rhs_ext.qry.length-self.rhs_ext.qry.start+1,
                                     self.rhs_ext.qry.length)))
        bpoint_f = self.rhs_ext.ref.stop + self.rhs_ext.ref.aln_length+1
        bpoint_r = self.rhs_ext.qry.length-self.rhs_ext.qry.start + 1
      else:
        extseq = reads[self.rhs_ext.qry.sra_rowid][self.rhs_ext.qry.stop+1:]
        stdout.write(self.anneal_extension('rhs', reads[self.rhs_ext.qry.sra_rowid][self.rhs_ext.qry.stop+1:]))
        bpoint_f = self.rhs_ext.ref.stop + 1
        bpoint_r = self.rhs_ext.qry.stop + 1
      print("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.name,
                                                      'rhs',
                                                      bpoint_f,
                                                      self.rhs_ext.qry.sra_rowid,
                                                      bpoint_r,
                                                      isRevComp,
                                                      len(extseq),
                                                      extseq))
    if self.lhs_ext != None and (self.lhs_ext.qry.sra_rowid in reads):
      isRevComp = False
      extseq = ''
      bpoint_f = 0
      bpoint_r = 0
      if self.lhs_ext.ref.strand == 0 and self.lhs_ext.qry.strand == 1:
        isRevComp = True
        print("DOUBLE CHECK THIS")
        extseq = self.revcomp_seq(reads[self.lhs_ext.qry.sra_rowid],
                                  self.lhs_ext.qry.length-self.rhs_ext.qry.end+1,
                                  self.lhs_ext.qry.length)
        stdout.write(self.anneal_extension('lhs', self.revcomp_seq(reads[self.lhs_ext.qry.sra_rowid],
                                                      self.lhs_ext.qry.length-self.rhs_ext.qry.end+1,
                                                      self.lhs_ext.qry.length)))
        bpoint_f = self.lhs_ext.ref.start - 1
        bpoint_r = self.lhs_ext.qry.start - 1
      else:
        extseq = reads[self.lhs_ext.qry.sra_rowid][:self.lhs_ext.qry.start-1]
        stdout.write(self.anneal_extension('lhs', reads[self.lhs_ext.qry.sra_rowid][:self.lhs_ext.qry.start-1]))
        bpoint_f = self.lhs_ext.ref.start - 1
        bpoint_r = self.lhs_ext.qry.start - 1
      print("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.name,
                                                      'lhs',
                                                      bpoint_f,
                                                      self.lhs_ext.qry.sra_rowid,
                                                      bpoint_r,
                                                      isRevComp,
                                                      len(extseq),
                                                      extseq))
  def anneal_extension(self, flank, extseq):
    if flank == 'lhs':
      #self.lhs_ext_seq = lib.sequence.sequence.Sequence("ctg_{}_{}".format(self.name, flank),
                                                    #extseq + self.lhs.sequence)
      return ">{}_{}_ext\n{}\n".format(self.name, flank, extseq+self.lhs.sequence)
      #print(self.lhs_ext_seq.name, self.lhs_ext_seq.sequence)
    if flank == 'rhs':
      #self.rhs_ext_seq = lib.sequence.sequence.Sequence("ctg_{}_{}".format(self.name, flank),
       #                                             self.rhs.sequence + extseq)
      #print(self.rhs_ext_seq.name, self.rhs_ext_seq.sequence)
      return ">{}_{}_ext\n{}\n".format(self.name, flank, extseq+self.rhs.sequence)

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
