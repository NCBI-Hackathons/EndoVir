#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  endovir.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import os
import sys
import argparse
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.blastdb.makeblastdb
import lib.blast.blastdb.makeprofiledb


import screener
import virus_contig

class Endovir:

  def __init__(self, wd=None):
    self.analysis_path = ''
    self.dbs_path =  ''
    self.wd = os.getcwd() if wd == None else wd
    self.screens = {}
    self.flank_len = 500
    self.dbs_dirname = 'dbs'
    self.db_sources = {
      'virusdb' : {'src' : 'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.1.genomic.fna.gz',
                      'db'  : lib.blast.blastdb.makeblastdb.Makeblastdb(name='viral.genomic.refseq.fna',
                                                                  dbdir=os.path.join(self.wd, self.dbs_dirname),
                                                                  typ='nucl')},
          'cdd'    : {'src' : 'ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz',
                      'db'  : lib.blast.blastdb.makeprofiledb.Makeprofiledb(name='cdd',
                                                                      dbdir=os.path.join(self.wd, self.dbs_dirname),
                                                                      typ='rps')}
                      }
    self.dbs = {}

  def set_wd(self):
    if not os.path.isdir(self.wd):
      os.mkdir(self.wd)

  def setup(self):
    self.set_wd()
    self.setup_databases()

  def setup_databases(self):
    if not os.path.isdir(os.path.join(self.wd, self.dbs_dirname)):
      os.mkdir(os.path.join(self.wd, self.dbs_dirname))
    for i in self.db_sources:
      print("Setup Blast DB {0}".format(i), file=sys.stderr)
      self.dbs[i] = self.db_sources[i]['db']
      self.dbs[i].setup(src=self.db_sources[i]['src'])

  def screen(self, srrs=[]):
    vrs_ctgs = {}
    for i in srrs:
      print("Screening {0}".format(i), file=sys.stderr)
      s = screener.Screener(self.wd, i, self.dbs['virusdb'], self.dbs['cdd'])
      srr_alignments = s.screen_srr(s.srr, s.virus_db.path)
      vdb_parser = s.vdbdump.run(s.srr, srr_alignments)
      contigs = s.assemble(vdb_parser.dump_to_file())
      for j in s.cdd_screen(contigs, s.cdd_db.path, os.path.join(s.wd,'rpst')):
        c = virus_contig.VirusContig("ctg_"+str(len(vrs_ctgs)),
                                     s.assembler.parser.sequences[j].sequence,
                                     i,
                                     s.assembler.parser.sequences[j].header,
                                     self.flank_len,
                                     s.wd)
        vrs_ctgs[c.name] = c
      s.bud(vrs_ctgs, self.flank_len)

def main():
  #srrs = ['SRR5150787']
  srrs = ['SRR5832142']
  ev = Endovir(wd='analysis')
  ev.setup()
  ev.screen(srrs)
  return 0

if __name__ == '__main__':
  main()
