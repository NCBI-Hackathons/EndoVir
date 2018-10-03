#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------


import io
import os
import sys

class ContigDatabase:

  def __init__(self, screen):
    self.contigs_map = {}
    self.flank_ratio = 0.25  # How much flanking sequence should be used to align flanks to srr

  def add_contig(self, contig):
    self.contigs_map[contig.name] = contig
    return contig

  def get_contigs(self):
    return [self.contigs_map[x] for x in self.contigs_map]
