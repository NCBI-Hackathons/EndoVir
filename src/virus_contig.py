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
import flanker

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
    self.flanker = flanker.Flanker(flank_len)
    self.assembler = lib.megahit.megahit.Megahit()
    #self.vdbdump = lib.vdbdump.vdbdump.VdbDump()
    self.iteration = 0
    self.wd = os.path.join(screen_dir, self.name)
    if not os.path.exists(self.wd):
      os.mkdir(self.wd)

  def extend(self, assembler, flank_alignments):
    print(self.wd, self.src.srr, self.name, len(flank_alignments))
    vdbdump = lib.vdbdump.vdbdump.VdbDump()
    vdb_parser = vdbdump.run(self.src.srr, flank_alignments)
    vdb_parser.dump_to_file(fout='ext.fq')
    ext_asm = os.path.join(self.wd, 'asm.reads.'+str(self.iteration)+'.fifo')
    ext_asm_fh  = open(ext_asm, 'w')
    for i in vdb_parser.sequences:
       ext_asm_fh.write(vdb_parser.sequences[i].get_sequence())
    ext_asm_fh.write(">"+self.name+'\n'+self.sequence)
    ext_asm_fh.close()
    asm = assembler.new()
    asm.run(ext_asm, prefix=self.name, outdir=os.path.join(self.wd, 'asm'+str(self.iteration)))
    #update self.length, self.assembly, sefl.flanks
    #os.unlink(asm_reads)

  def extract_flanks(self, stdout):
    self.flanker.extract_flanks(self)
    if len(self.flanker.rhs.sequence) > 0:
      stdout.write(self.flanker.rhs.get_sequence())
    stdout.write(self.flanker.lhs.get_sequence())

  def update(self, sequence):
    self.sequence = sequence
    self.length = len(sequence)
