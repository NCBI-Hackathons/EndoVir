#  flank_rhs.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from . import flank

class RhsFlank(flank.Flank):

  def __init__(self, contig):
    super().__init__(contig, 'rhs')
    self.ref_overlap = 20
    self.qry_overlap = 20

  def get_fasta_sequence(self):
    return ">{}\n{}\n".format(self.name, self.contig.sequence[-self.length:])

  def calc_extension_length(self, alignment):
    return alignment.qry.length - alignment.qry.stop + 1

  def update_extension(self, alignment):
    if self.calc_extension_length(alignment) > self.overlap.length:
      self.overlap.update(alignment, self.calc_extension_length(alignment))
      return True
    return False

  def check_overlap(self, alignment):
    if (alignment.ref.get_ordered_coords()[1] > (self.length - self.ref_overlap)) and \
       (alignment.qry.get_ordered_coords()[1] < alignment.qry.length - self.qry_overlap):
      return self.update_extension(alignment)
    return False

  def get_extension(self, reads):
    if self.overlap.isRevCompl:
      print("DOUBLE CHECK THIS")
      print(">{}\n{} - {}\n".format(self.name, -self.length, self.overlap.alignment.ref.stop))
      print(">{}\n{} - {}\n".format(self.overlap.alignment.qry.sra_rowid,
                                    self.overlap.alignment.qry.
                                    start, self.overlap.alignment.qry.length))
      print(">{}\n{}\n".format(self.overlap.alignment.qry.sra_rowid, self.mk_revcompl(reads[self.overlap.alignment.qry.sra_rowid],
                                  self.overlap.alignment.qry.start,
                                  self.overlap.alignment.qry.length)))

      extseq = self.contig.sequence[-self.length:self.overlap.alignment.ref.stop] \
               + self.mk_revcompl(reads[self.overlap.alignment.qry.sra_rowid],
                                  self.overlap.alignment.qry.start,
                                  self.overlap.alignment.qry.length)
      print(extseq)

      return self.Extension("{}_ext".format(self.name),
                            extseq,
                            self.overlap.alignment.ref.stop,
                            self.overlap.alignment.qry.start)

    print(">{}\n{}\n".format(self.overlap.alignment.qry.sra_rowid,
                             reads[self.overlap.alignment.qry.sra_rowid][self.overlap.alignment.qry.start:]))
    extseq = self.contig.sequence[self.contig.length-self.length:self.contig.length-self.length+self.overlap.alignment.ref.stop] \
              + reads[self.overlap.alignment.qry.sra_rowid][self.overlap.alignment.qry.start+1:]
    return self.Extension("{}_ext".format(self.name),
                          extseq,
                          self.overlap.alignment.ref.stop,
                          self.overlap.alignment.qry.start)
