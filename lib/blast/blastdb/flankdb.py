#  flankdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

from . import database

class FlankDb(database.BlastDatabase):

  def __init__(self, dbdir, dbname):
    super().__init__(dbdir=dbdir, name=dbname, cmd='makeblastdb', typ='nucl')
    self.refs = {}

  def mux(self, contigs):
    self.refs = {}
    rfd, wfd = os.pipe()
    stdout = os.fdopen(wfd, 'w')
    for i in contigs:
      contigs[i].extract_flanks(stdout)
      self.refs[i.split(':')[0]] = []
    stdout.close()
    stdin = os.fdopen(rfd, 'r')
    self.make_db_stdin(stdin)
    stdin.close()

  def demux(self, srr_parser):
    for i in srr_parser.alignments:
      if i.ref.name.split(':')[0] in self.refs:
        self.refs[i.ref.name.split(':')[0]].append(i.qry.name)

    print(len(srr_parser.alignments))
    for i in self.refs:
      print(i, len(self.refs[i]))
