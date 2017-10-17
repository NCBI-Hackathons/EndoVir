#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  endovir.py
#
#  Copyright 2017 USYD
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import os
import sys
import argparse
import urllib.request
import urllib.error
import gzip

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blastdb.makeblastdb
import lib.blastdb.makeprofiledb
#from . import bud.Bud

class Endovir:

  def __init__(self, wd=None):
    self.analysis_path = ''
    self.dbs_path =  ''
    self.anlyses = []
    self.wd = os.getcwd() if wd == None else wd
    self.dbs_dirname = 'dbs'
    self.db_sources = {
      'vrs_refseq' : {'src' : 'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.1.genomic.fna.gz',
                      'db'  : lib.blastdb.makeblastdb.Makeblastdb(name='vrs_refseq',
                                                                  dbdir=os.path.join(self.wd, self.dbs_dirname),
                                                                  typ='nucl')},
          'cdd'    : {'src' : 'ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz',
                      'db'  : lib.blastdb.makeprofiledb.Makeprofiledb(name='cdd',
                                                                      dbdir=os.path.join(self.wd, self.dbs_dirname),
                                                                      typ='rps')}
                      }
    self.dbs = {}

  def set_wd(self):
    if not os.path.isdir(self.wd):
      os.makedir(self.wd)

  def setup(self):
    self.set_wd()
    self.setup_databases()

  def setup_databases(self):
    if not os.path.isdir(os.path.join(self.wd, self.dbs_dirname)):
      os.makedir(os.path.join(self.wd, self.dbs_dirname))

    for i in self.db_sources:
      print("Setup Blast DB {0}".format(i), file=sys.stderr)
      self.dbs[i] = self.db_sources[i]['db']
      self.dbs[i].setup(src=self.db_sources[i]['src'])


def main():
  srr = 'SRR5150787'
  ev = Endovir(wd='analysis')
  ev.setup()
  return 0

if __name__ == '__main__':
  main()
