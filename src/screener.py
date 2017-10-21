#  screen.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#

import os
import sys
import shutil
sys.path.insert(1, os.path.join(sys.path[0], '../'))

import lib.blast.blastdb.makeblastdb
import lib.blast.magicblast.magicblast
import lib.megahit.megahit
import lib.blast.rps.rpstblastn
import lib.vdbdump.vdbdump

import bud

class Screener:

  def __init__(self, wd, srr, virus_db, cdd_db):
    self.wd = os.path.join(wd, srr)
    if not os.path.exists(self.wd):
      os.makedir(self.wd)
    self.srr = srr
    self.virus_db = virus_db
    self.cdd_db = cdd_db
    self.asm = self.srr
    if os.path.exists(os.path.join(self.wd, 'asm')):
      shutil.rmtree(os.path.join(self.wd, 'asm'))
    self.asm_dir = os.path.join(self.wd, 'asm')
    self.asm_contigs = None
    self.assembler = lib.megahit.megahit.Megahit()
    self.srascreener = lib.blast.magicblast.magicblast.Magicblast()
    self.cdd_screener = lib.blast.rps.rpstblastn.RpstBlastn()

  def screen_srr(self, srr, db):
    self.srascreener.run(srr, db)

  def assemble(self, sequences):
    return self.assembler.run(sequences, prefix=self.asm, outdir=self.asm_dir)

  def cdd_screen(self, contigs, db, outf):
    return self.cdd_screener.run(contigs, db, outf)

  def bud(self, contigs):
    b = bud.Buddy(wd=self.wd)
    b.bud(self.srr, contigs)
