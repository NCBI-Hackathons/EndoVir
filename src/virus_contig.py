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
    self.wd = os.path.join(screen_dir, self.name)
    if not os.path.exists(self.wd):
      os.mkdir(self.wd)

    #print(self.src, self.srr, self.flank_len, self.wd)

  def extend(self, alignments):
    vdbdump = lib.vdbdump.vdbdump.VdbDump()
    for i in alignments:
      print(i)
    pass


  #def identify_overlaps(self, cols):
    #qbeg = int(cols[6])
    #qend = int(cols[7])
    #rbeg = int(cols[8])
    #rend = int(cols[9])
    #qlen = int(cols[15])
    #if cols[13] == 'minus':    # query is minus, reference is plus
      #qbeg, qend = qend, qbeg
    #if cols[14] == 'minus':  # Reference is minus , query is plus
      #rbeg, rend = rend, rbeg
    #if self.hasBothFlanks == False:
        #if rbeg > 10 and rend < self.flank_len - 10:
          #pass
        #else:
          #self.alignments.append(magicblast_alignment.MagicblastAlignment(cols))
    #else:
      #if cols[1].split(':')[1] ==  'rhs':
        #if rbeg > contigs[cnt].flank_len - qlen and qend < qlen-10:
          #self.alignments.append(magicblast_alignment.MagicblastAlignment(cols))
          ##print("extend right")
      #else:
        #if rbeg <= 10 and qbeg >= 10:
          #self.alignments.append(magicblast_alignment.MagicblastAlignment(cols))
          ##print("extend right")
    ##print("======================")

  #def parse(self, src, contigs):
    #self.alignments = []
    #read_count = 0
    #for i in src:
      #self.identify_overlaps(i.strip().split('\t'), contigs)
      ##self.alignments.append(magicblast_alignment.MagicblastAlignment(i.strip().split('\t')))
      #read_count  += 1
    #print("Init reads:", read_count)
    #return self.alignments

  #def bud(self):
    #self.screen_flanks()

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
