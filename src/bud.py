#  bud.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#   The Python implementation of ViruSpy [0] to allow better control of
#   MagicBLAST [1].
#
# [0] https://github.com/NCBI-Hackathons/ViruSpy
# [1] ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/1.0.0
#  Version: 0.0

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.blastdb.makeblastdb
import lib.blast.magicblast.magicblast
#import lib.vdbdump.vdbdump
#import lib.megahit.megahit

import flanker

class Buddy:

  def __init__(self, wd):
    self.wd = wd
    self.len_flank = 500
    #self.vbddump =  lib.vdbdump.vdbdump.VdbDump()
    #self.assembler = lib.megahit.megahit.Megahit()
    self.flank_db = "flanks"

  def screen_srr(self, srr, db):
    m = lib.blast.magicblast.magicblast.Magicblast()
    m.run(srr, db)

  def assemble(self, flanks):
    print("Running meggahit with flanking sequences", file=sys.stderr)
    self.assembler.out_prefix = srr
    mgh.out_dir = srr+"_megahit"
    mgh.run(flanks)

  def make_flankdb(self, contigs):
    f = flanker.Flanker()
    db_flanks = lib.blast.blastdb.makeblastdb.Makeblastdb(dbdir=self.wd, name=self.flank_db, typ='nucl')
    p = db_flanks.make_db_from_stdin()
    for i in contigs:
      p.stdin.write(str.encode(f.add_sequence(i, stream=True)))
    p.stdin.flush()
    p.stdin.close()
    return db_flanks

  def bud(self, srr, contigs):
    iteration = 0
    while True:
      db = self.make_flankdb(contigs)
      #self.screen_srr(srr, db.path)
      #self.assemble()
      iteration += 1
      if iteration == 1: # only for initial testing  purposes.
        break
