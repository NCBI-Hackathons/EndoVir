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
import lib.megahit.megahit
import lib.blast.rps.rpstblastn
import lib.vdbdump.vdbdump
import flankdb

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

  def bud(self, contigs):
    while True:
      self.flankdb.mux(contigs)
      srr_screener = lib.blast.magicblast.magicblast.Magicblast()
      fp = lib.blast.magicblast.magicblast_flank_parser.MagicblastFlankParser()
      alignments = fp.parse(srr_screener.run(self.srr, self.flankdb.path),contigs)
      self.flankdb.demux(alignments)
      for i in  self.flankdb.refs:
        for j in self.flankdb.refs[i][:3]:
          print(i, j.btop, j.qry.name, j.qry.start, j.ref.name, j.ref.start)
      #for i in contigs:
      #  if i in self.flankdb.refs:
      #    print("Contig {0}: extending reads: {1}".format(i, len(self.flankdb.refs[i])))
      #    contigs[i].extend(self.assembler, self.flankdb.refs[i])
        #contigs[i].iteration += 1
        #return
      sys.exit()

  def check_contig_overlaps(self):
    pass
