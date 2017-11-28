#  flankdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../../'))
import lib.sequence
import lib.blast.blastdb.database


class FlankDb(lib.blast.blastdb.makeblastdb.Makeblastdb):

  def __init__(self, dbdir, dbname):
    super().__init__(dbdir=dbdir, name=dbname, typ='nucl')
    self.refs = {}

  def mux(self, contigs):
    self.refs = {}
    rfd, wfd = os.pipe()
    stdout = os.fdopen(wfd, 'w')
    for i in contigs:
      stdout.write(self.extract_contig_flanks(contigs[i]))
      self.refs[i.split(':')[0]] = []
    stdout.close()
    stdin = os.fdopen(rfd, 'r')
    self.make_db_stdin(stdin)
    stdin.close()
    return True

  def demux(self, alignments):
    for i in alignments:
      if i.ref.name.split(':')[0] in self.refs:
        self.refs[i.ref.name.split(':')[0]].append(i)


  def extract_contig_flanks(self, contig):
    if contig.length <= contig.flank_len:
      contig.lhs = lib.sequence.sequence.Sequence(self.name+":lhs", contig.subseq(0, contig.length))
      return ">{}\n{}\n".format(contig.lhs.name, contig.lhs.sequence)
    else:
      contig.lhs = lib.sequence.sequence.Sequence(contig.name+":lhs", contig.subseq(0, contig.flank_len))
      contig.rhs = lib.sequence.sequence.Sequence(contig.name+":rhs", contig.subseq(contig.length-contig.flank_len,
                                                             contig.flank_len))
      return ">{}\n{}\n>{}\n{}\n".format(contig.lhs.name, contig.lhs.sequence,
                                         contig.rhs.name, contig.rhs.sequence)
