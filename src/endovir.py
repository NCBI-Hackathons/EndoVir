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
import lib.blastdb.blastdb
import lib.blastdb.makeprofiledb

from . import bud

class Endovir:

  def __init__(self):
    self.analysis_path = ''
    self.dbs_path =  ''
    self.anlyses = []
    self.wd = None
    self.dbs_dirname = 'dbs'
    self.db_sources = {
                        'vrs_refseq' : {'src': 'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.nonredundant_protein.1.protein.faa.gz',
                                    'dbtype' : 'nucl',
                                    'tool'   : lib.blastdb.blastdb.Makeblastdb()},
                        'cdd'    : {'src' : 'ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/little_endian/Cdd_NCBI_LE.tar.gz',
                                    'dbtype' : 'rps',
                                    'tool' : lib.blastdb.makeprofiledb.Makeprofiledb()}
                      }
    self.dbs = {}

  def set_wd(self, wd):
    if wd == None:
      self.wd = os.getcwd()
    else:
      self.wd = wd
      if not os.path.isdir(self.wd):
        os.makedir(self.wd)

  def setup(self, wd=None):
    self.set_wd(wd)
    self.setup_databases(self)

  def setup_databases(self):
    if not os.path.isdir(os.path.join(self.wd, self.db_dirname))
      os.makedir(os.path.join(self.wd, self.dbs_dirname))
    for i in self.db_sources:
      self.db_sources[i]['tool'].setup(path=os.path.join(self.wd, self.dbs_dirname), title=i)


def main():

  return 0

if __name__ == '__main__':
  main()
