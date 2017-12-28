#  screen.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#

import os
import sys
import shutil
import time

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.magicblast.magicblast
import lib.blast.magicblast.magicblast_parser
import lib.blast.magicblast.magicblast_flank_parser
import lib.blast.blastn.blastn
import lib.blast.blastdb.makeblastdb
import lib.megahit.megahit
import lib.blast.rps.rpstblastn
import lib.vdbdump.vdbdump

import flankdb
from flanks import flank_checker

class Linker:

  def __init__(self):
    self.flank_map = {}
    self.contig_map = {}
    self.extension_map = {}

  def add_contig(self, contig):
    self.contig_map[contig.name] = contig
    self.flank_map[contig.lhs_flank.name] = contig.lhs_flank
    self.flank_map[contig.rhs_flank.name] = contig.rhs_flank
    self.extension_map[contig.lhs_flank.extension.name] = contig.lhs_flank.extension
    self.extension_map[contig.rhs_flank.extension.name] = contig.rhs_flank.extension

  def extension_to_flank(self, extension):
    if extension.name in self.extension_map:
      return self.extension_map[self.extension_map.name].flank
    return None

  def extension_to_contig(self, extension):
    if extension.name in self.extension_map:
      return self.flank_to_contig(self.extension_to_flank(extension))
    return None

  def flank_to_contig(self, flank):
    if flank.name in self.flank_map:
      return self.flank_map[flank.name].contig
    return None

  def get_flank(self, name):
    if name in self.flank_map:
      return self.flank_map[name]
    if name in self.extension_map:
      return self.extension_map[name].flank

  def get_extension(self, extension_name):
    return self.extension_map.get(extension_name)

  def get_contig(self, name):
    if name in self.contig_map:
      return self.contig_map[contig]
    if name in self.extension_map:
      return  self.extension_map[name].flank.contig
    if name in self.flank_map:
      return  self.flank_map[name].contig

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
    lnk = Linker()
    for i in contigs:
      lnk.add_contig(contigs[i])

    while True:
      while self.flankdb.collect_flanks(contigs) != True:
        time.sleep(0.01)
      mb = lib.blast.magicblast.magicblast.Magicblast()
      fp = lib.blast.magicblast.magicblast_flank_parser.MagicblastFlankParser(self.flankdb.flankmap)
      extensions = fp.parse(mb.run(self.srr, self.flankdb.path), contigs)
      reads = self.vdbdump.rowids_to_reads(self.srr, [x.read.sra_rowid for x in extensions])
      rfd, wfd = os.pipe()
      stdout = os.fdopen(wfd, 'w')
      ext_rowids = []
      for i in contigs:
        contigs[i].extend(reads)
        contigs[i].save_fasta()
        stdout.write(contigs[i].get_flanks())
        if contigs[i].lhs_flank.extension.sra_rowid != 0:
          ext_rowids.append(contigs[i].lhs_flank.extension.sra_rowid)
        if contigs[i].rhs_flank.extension.sra_rowid != 0:
          ext_rowids.append(contigs[i].rhs_flank.extension.sra_rowid)
        contigs[i].show()
      stdout.close()
      for i in ext_rowids:
        print("vdb-dump {0} -R {1} -f fasta > {1}.fa".format(self.srr, i), file=sys.stderr)
      self.check_flank_overlaps(rfd, contigs, lnk)
      print(len(contigs))
      sys.exit()
      if len(contigs) < 2:
        break

  def check_flank_overlaps(self, rfd, contigs, lnk):
    print("Checking flanks for overlaps")
    blastn = lib.blast.blastn.blastn.BlastN()
    stdin = os.fdopen(rfd, 'r')
    ph = blastn.run(self.flankdb.path, stdin)
    stdin.close()
    fc = flank_checker.FlankChecker()
    fc.parse(ph.stdout)
    fc.check(contigs, lnk)
    for i in fc.updates:
      print(i, fc.updates[i].name)
