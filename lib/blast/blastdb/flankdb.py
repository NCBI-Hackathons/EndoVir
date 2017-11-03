#  flankdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys



sys.path.insert(1, os.path.join(sys.path[0], '../../'))
import lib.fasta.sequence
from . import database

def extract_flanks(self, stdout):
    self.flanker.extract_flanks(self)
    if len(self.flanker.rhs.sequence) > 0:
      stdout.write(self.flanker.rhs.get_sequence())
    stdout.write(self.flanker.lhs.get_sequence())


class FlankDb(database.BlastDatabase):

  class Flank(lib.fasta.sequence.FastaSequence):

    def __init__(self, name, seq, location):
      super().__init__(name, seq)
      self.location = location

  def __init__(self, dbdir, dbname):
    super().__init__(dbdir=dbdir, name=dbname, cmd='makeblastdb', typ='nucl')
    self.refs = {}
    self.flanks = {}

  def mux(self, contigs):
    self.refs = {}
    rfd, wfd = os.pipe()
    stdout = os.fdopen(wfd, 'w')
    for i in contigs:
      self.extract_contig_flanks(contigs[i], stdout)
      self.refs[i.split(':')[0]] = []
    stdout.close()
    stdin = os.fdopen(rfd, 'r')
    self.make_db_stdin(stdin)
    stdin.close()

  def demux(self, alignments):
    for i in alignments:
      if i.ref.name.split(':')[0] in self.refs:
        self.refs[i.ref.name.split(':')[0]].append(i)

  def extract_contig_flanks(self, contig, stdout):
    if contig.length <= contig.flank_len:
      contig.lhs = self.Flank(contig.name+":lhs", contig.subseq(0, contig.length), 'lhs')
      stdout.write(contig.lhs.get_sequence())
    else:
      contig.lhs = self.Flank(contig.name+":lhs", contig.subseq(0, contig.flank_len), 'lhs')
      stdout.write(contig.lhs.get_sequence())
      contig.rhs = self.Flank(contig.name+":rhs",
                              contig.subseq(contig.length-contig.flank_len,
                                            contig.flank_len, contig.name+"_rhs"),
                              'rhs')
      stdout.write(contig.rhs.get_sequence())
