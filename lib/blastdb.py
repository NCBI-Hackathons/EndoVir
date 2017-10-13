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

  def __init__(self, path='', typ='nucl'):
    self.cmd = 'makeblastdb'
    self.typ = typ
    self.path = path

  def make_db(self, filepath):
    # Would love to pipe the sequences into makeblastdb but need to figure out
    # how to pass a stream into a method
    #subprocess.Popen([self.cmd, '-dbtype', self.typ,
                              #'-in', filepath,
                              #'-out', self.path],
                                       #stdout=subprocess.PIPE,
                                       #bufsize=1)
    subprocess.run([self.cmd, '-dbtype', self.typ,
                              '-in', filepath,
                              '-out', self.path])
