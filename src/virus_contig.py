#  contig.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

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

  def __init__(self, name, seq, src_srr, src_contig, flank_len, srr_dir):
    super().__init__(name, seq)
    self.src = self.Source(src_srr, src_contig)
    self.assembly = self.Assembly()
    self.flanker = flanker.Flanker(flank_len)
    self.assembler = lib.megahit.megahit.Megahit()
    self.vdbdump = lib.vdbdump.vdbdump.VdbDump()
    self.iteration = 0
    self.wd = os.path.join(srr_dir, self.name)

  def extend(self, assembler, reads):
    #print(self.src.srr, self.src.contig, len(reads))
    print(self.src.srr, self.name, 'asm'+str(self.iteration))
    self.vdbdump.run(self.src.srr, reads)
    if not os.path.exists(os.path.join(self.src.srr, self.name, 'asm'+str(self.iteration))):
      os.makedirs(os.path.join(self.wd, self.src.srr, 'asm'+str(self.iteration)))
    asm = assembler.new(os.path.join(self.wd, self.src.srr, 'asm'+str(self.iteration)))
    #reads = os.join(self.wd, 'asm'+str(self.iteration), 'reads.fifo')
    #os.mkfifo(reads)
    #fifo =open(fifo, 'w')
    #fifo.write(self.contig.get_sequence())
    #fifo.write(self.contig.get_sequence())
    #asm.run() self.seq +  reads
    #update self.length, self.assembly, sefl.flanks

  def extract_flanks(self, stdout):
    self.flanker.extract_flanks(self)
    if len(self.flanker.rhs.sequence) > 0:
      stdout.write(self.flanker.rhs.get_sequence())
    stdout.write(self.flanker.lhs.get_sequence())
