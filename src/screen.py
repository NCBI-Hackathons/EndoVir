#  screen.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#

import os
import sys
import shutil

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import flanker
import lib.blast.blastdb.makeblastdb
import lib.blast.magicblast.magicblast
import lib.megahit.megahit
import lib.blast.rps.rpstblastn

class Screen:

  def __init__(self, wd, srr, virus_db, cdd_db):
    self.iteration = 0
    self.wd = os.path.join(wd, srr, str(self.iteration))
    if not os.path.exists(self.wd):
      os.makedirs(self.wd)
    self.srr = srr
    self.virus_db = virus_db
    self.cdd_db = cdd_db
    self.iteration = 0
    self.aligned_srr = os.path.join(self.wd,'aligned_srr.fq')
    self.contigs = []
    self.flanks = []
    self.asm = self.srr+str(self.iteration)
    if os.path.exists(os.path.join(self.wd, 'asm')):
      shutil.rmtree(os.path.join(self.wd, 'asm'))
    self.asm_dir = os.path.join(self.wd, 'asm')
    self.asm_contigs = None
    self.assembler = lib.megahit.megahit.Megahit()
    self.srascreener = lib.blast.magicblast.magicblast.Magicblast()
    self.cdd_screener = lib.blast.rps.rpstblastn.RpstBlastn()

  def screen_srr(self, srr, db):
    self.srascreener.run(srr, db, self.aligned_srr)

  def assemble(self, sequences):
    self.asm_contigs = self.assembler.run(sequences, prefix=self.asm, outdir=self.asm_dir)

  def protein_screen(self, contigs, db, outf):
    self.cdd_screener.run(contigs, db, outf)

  def create_flanks(self):
    pass

  def bud(self):
    pass
