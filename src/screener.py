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
import lib.blast.blastdb.makeblastdb
import lib.megahit.megahit
import lib.blast.rps.rpstblastn
import lib.vdbdump.vdbdump

import flankdb
import flank_chk

class Linker:

  def __init__(self):
    self.flank_map = {}
    self.contig_map = {}
    self.overlap_map = {}

  def add_contig(self, contig):
    self.contig_map[contig.name] = contig
    self.flank_map[contig.lhs_flank.name] = contig.lhs_flank
    self.flank_map[contig.rhs_flank.name] = contig.rhs_flank
    self.overlap_map[contig.lhs_flank.overlap.name] = contig.lhs_flank.overlap
    self.overlap_map[contig.rhs_flank.overlap.name] = contig.rhs_flank.overlap

  def overlap_to_flank(self, overlap):
    if overlap.name in self.overlap_map:
      return self.overlap_map[self.overlap_map.name].flank
    return None

  def overlap_to_contig(self, overlap):
    if overlap.name in self.overlap_map:
      return self.flank_to_contig(self.overlap_to_flank(overlap))
    return None

  def flank_to_contig(self, flank):
    if flank.name in self.flank_map:
      return self.flank_map[flank.name].contig
    return None

  def get_flank(self, name):
    if name in self.flank_map:
      return self.flank_map[name]
    if name in self.overlap_map:
      return self.overlap_map[name].flank

  def get_overlap(self, overlap_name):
    return self.overlap_map.get(overlap_name)

  def get_contig(self, name):
    if name in self.contig_map:
      return self.contig_map[contig]
    if name in self.overlap_map:
      return  self.overlap_map[name].flank.contig
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

  def find_extensions(self, contigs):
    pass

  def flank_to_contig(self, flank):
    pass

  def bud(self, contigs):
    lnk = Linker()
    for i in contigs:
      lnk.add_contig(contigs[i])

    while True:
      while self.flankdb.collect_flanks(contigs) != True:
        time.sleep(0.0001)
      mb = lib.blast.magicblast.magicblast.Magicblast()
      fp = lib.blast.magicblast.magicblast_flank_parser.MagicblastFlankParser(self.flankdb.flankmap)
      extensions = fp.parse(mb.run(self.srr, self.flankdb.path), contigs)
      reads = self.vdbdump.rowids_to_reads(self.srr, [x.qry.sra_rowid for x in extensions])
      rfd, wfd = os.pipe()
      stdout = os.fdopen(wfd, 'w')
      contig = lib.blast.blastdb.makeblastdb
      for i in contigs:
        ext = contigs[i].get_extensions(reads)
        if contigs[i].hasExtension:
          fh = open(os.path.join(contigs[i].wd, contigs[i].name+'.fa'), 'w')
          fh.write(">{}\n{}\n".format(contigs[i].name, contigs[i].sequence))
          fh.close()
          fh = open(contigs[i].name+'_ext.fa', 'w')
          fh.write(ext)
          fh.close()
          stdout.write(ext)
      stdout.close()
      stdin = os.fdopen(rfd, 'r')
      blastn = lib.blast.blastn.blastn.BlastN()
      ph = blastn.run(self.flankdb.path, stdin)
      stdin.close()
      self.check_flank_overlaps(ph, contigs, lnk)
      stdin.close()
      sys.exit()

  def check_flank_overlaps(self, blast_proc, contigs, lnk):
    fc = flank_chk.FlankChecker()
    fc.parse(blast_proc.stdout)
    fc.check(contigs, lnk)
