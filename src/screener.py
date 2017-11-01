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

import lib.blast.blastdb.flankdb
import lib.blast.magicblast.magicblast
import lib.blast.magicblast.magicblast_flank_parser
import lib.megahit.megahit
import lib.blast.rps.rpstblastn
import lib.vdbdump.vdbdump

import bud

class Screener:

  def __init__(self, wd, srr, virus_db, cdd_db):
    if not os.path.exists(os.path.join(wd, srr)):
      os.mkdir(os.path.join(wd, srr))
    self.wd = os.path.join(wd, srr)
    self.srr = srr
    self.virus_db = virus_db
    self.cdd_db = cdd_db
    self.asm = self.srr
    if os.path.exists(os.path.join(self.wd, 'asm')):
      shutil.rmtree(os.path.join(self.wd, 'asm'))
    self.asm_dir = os.path.join(self.wd, 'asm')
    self.asm_contigs = None
    self.assembler = lib.megahit.megahit.Megahit()
    self.vdbdump = lib.vdbdump.vdbdump.VdbDump()
    self.srascreener = lib.blast.magicblast.magicblast.Magicblast()
    self.cdd_screener = lib.blast.rps.rpstblastn.RpstBlastn()
    self.flankdb_dir = 'flanks'
    self.flankdb = lib.blast.blastdb.flankdb.FlankDb(dbdir=os.path.join(self.wd, self.flankdb_dir),
                                                     dbname='flanks')
    self.contigs = {}

  def screen_srr(self, srr, db):
    return self.srascreener.run(srr, db)

  def assemble(self, sequences):
    return self.assembler.run(sequences, prefix=self.asm, outdir=self.asm_dir)

  def cdd_screen(self, contigs, db, outf):
    return self.cdd_screener.run(contigs, db, outf)

  def bud(self, contigs):
    while True:
      self.flankdb.mux(contigs)
      self.flankdb.demux(self.srascreener.run(self.srr, self.flankdb.path, parser=lib.blast.magicblast.magicblast_flank_parser.MagicblastFlankParser()))
      for i in contigs:
        if i in self.flankdb.refs:
          print(i, len(self.flankdb.refs[i]))
          contigs[i].extend(self.assembler, self.flankdb.refs[i])
        contigs[i].iteration += 1
      break
