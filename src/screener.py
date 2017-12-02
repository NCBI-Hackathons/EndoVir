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
import lib.blast.magicblast.magicblast
import lib.blast.magicblast.magicblast_parser
import lib.blast.magicblast.magicblast_flank_parser
import lib.blast.blastn.blastn
import lib.megahit.megahit
import lib.blast.rps.rpstblastn
import lib.vdbdump.vdbdump

import flankdb
import flank_chk

class Screener:

  def __init__(self, wd, srr, virus_db, cdd_db):
    if not os.path.exists(os.path.join(wd, srr)):
      os.mkdir(os.path.join(wd, srr))
    self.wd = os.path.join(wd, srr)
    self.srr = srr
    self.virus_db = virus_db
    self.cdd_db = cdd_db
    if os.path.exists(os.path.join(self.wd, 'asm')):
      shutil.rmtree(os.path.join(self.wd, 'asm'))
    self.asm_dir = os.path.join(self.wd, 'asm')
    self.assembler = lib.megahit.megahit.Megahit()
    self.vdbdump = lib.vdbdump.vdbdump.VdbDump()
    self.cdd_screener = lib.blast.rps.rpstblastn.RpstBlastn()
    self.flankdb = flankdb.FlankDb(os.path.join(self.wd, 'flanks'), 'flanks')
    self.contigs = {}

  def screen_srr(self, srr, db):
    srr_screener = lib.blast.magicblast.magicblast.Magicblast()
    mbp = lib.blast.magicblast.magicblast_parser.MagicblastParser()
    mbp.parse(srr_screener.run(srr, db))
    return mbp.alignments

  def assemble(self, sequences):
    return self.assembler.run(sequences, prefix=self.srr, outdir=self.asm_dir)

  def cdd_screen(self, contigs, db, outf):
    return self.cdd_screener.run(contigs, db, outf)

  def find_extensions(self, contigs):
    pass

  def bud(self, contigs):
    while True:
      while self.flankdb.collect_flanks(contigs) != True:
        time.sleep(0.0001)
      mb = lib.blast.magicblast.magicblast.Magicblast()
      fp = lib.blast.magicblast.magicblast_flank_parser.MagicblastFlankParser(self.flankdb.flankmap)
      extensions = fp.parse(mb.run(self.srr, self.flankdb.path), contigs)
      reads = self.vdbdump.rowids_to_reads(self.srr, [x.qry.sra_rowid for x in extensions])
      print(reads)
      rfd, wfd = os.pipe()
      stdout = os.fdopen(wfd, 'w')
      for i in contigs:
        ext = contigs[i].get_extensions(reads)
        print(ext)
        stdout.write(ext)
      stdout.close()
      #stdin = os.fdopen(rfd, 'r')
      #self.check_flank_overlaps(self.flankdb.path, stdin, contigs)
      #stdin.close()
      sys.exit()

  def check_flank_overlaps(self, flank_db, stdin, contigs):
    blastn = lib.blast.blastn.blastn.BlastN()
    ph = blastn.run(flank_db, stdin)
    fc = flank_chk.FlankChecker()
    fc.parse(ph.stdout)
    fc.check(contigs)
