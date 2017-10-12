#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  blastdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import subprocess

class BlastDatabase:

  def __init__(self, db='', typ='nucl'):
    self.path = 'makeblastdb'
    self.typ = typ
    self.db = db

  def make_db(self, seqfile):
    subprocess.run([self.path], ['-dbtype'], [self.typ],
                                 ['-in'], [seqfile],
                                 ['-out'], self.db)
