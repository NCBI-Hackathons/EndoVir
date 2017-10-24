#  screen.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#

import os
import sys
import shutil
import  time
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
    self.flankdb = lib.blast.blastdb.makeblastdb.Makeblastdb(dbdir=self.wd,
                                                             name='flanks',
                                                             typ='nucl')

  def screen_srr(self, srr, db):
    self.srascreener.run(srr, db)

  def assemble(self, sequences):
    return self.assembler.run(sequences, prefix=self.asm, outdir=self.asm_dir)

  def cdd_screen(self, contigs, db, outf):
    return self.cdd_screener.run(contigs, db, outf)

  def screen_flanks(self, contigs):
    print("lalal", self.flankdb.path)
    rfd, wfd = os.pipe()
    stdout = os.fdopen(wfd, 'w')
    for i in contigs:
      i.extract_flanks(stdout)
    stdout.close()
    stdin = os.fdopen(rfd, 'r')
    self.flankdb.make_db_stdin(stdin)
    stdin.close()
    time.sleep(5)
    print("lalal", self.flankdb.path)
    self.srascreener.run(self.srr, self.flankdb.path)

  def bud(self, contigs):
    self.screen_flanks(contigs)
