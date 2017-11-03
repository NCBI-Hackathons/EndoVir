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
import lib.megahit.megahit
import lib.sequence.sequence
import lib.fasta.parser
#import flanker

class VirusContig(lib.sequence.sequence.Sequence):

  class Assembly:

    def __init__(self):
      self.N50 = 0

  class Source:

    def __init__(self, srr, contig):
      self.srr = srr
      self.contig = contig

  def __init__(self, name, seq, srr, src_contig, flank_len, screen_dir):
    super().__init__(name, seq)
    self.src = self.Source(srr, src_contig)
    self.assembly = self.Assembly()
    self.flank_len = flank_len
    self.iteration = 0
    self.wd = os.path.join(screen_dir, self.name)
    if not os.path.exists(self.wd):
      os.mkdir(self.wd)
    self.lhs = None
    self.rhs = None

  def extend(self, assembler, flank_alignments):
    cnt = open(self.name+'.fa', 'w')
    cnt.write(">"+self.name+"\n"+self.sequence)
    cnt.close()
    vdbdump = lib.vdbdump.vdbdump.VdbDump()
    vdb_parser = vdbdump.run(self.src.srr, flank_alignments)
    vdb_parser.dump_to_file(fout='ext.fq')
    ext_asm = os.path.join(self.wd, 'asm.reads.'+str(self.iteration)+'.fifo')
    ext_asm_fh  = open(ext_asm, 'w')
    for i in vdb_parser.sequences:
       ext_asm_fh.write(vdb_parser.sequences[i].get_sequence())
    ext_asm_fh.write(">"+self.name+'\n'+self.sequence+'\n')
    ext_asm_fh.close()
    asm = assembler.new()
    assembly = asm.run(ext_asm, prefix=self.name, outdir=os.path.join(self.wd, 'asm'+str(self.iteration)))
    self.asses(assembly)

  def update(self, assembly):
    p = lib.fasta.parser.FastaParser()
    p.parse(assembly)
    for i in p.sequences:
      self.sequence = p.sequences[i].sequence
      self.length = len(self.sequence)
      print("Update Iteration {0}:\nContig: {1}\tlen:{2}".format(self.iteration, self.name, self.length))

  def asses(self, assembly):
    print("Asses Iteration {0}:\nContig: {1}\tlen:{2}".format(self.iteration, self.name, self.length))
    self.update(assembly)
