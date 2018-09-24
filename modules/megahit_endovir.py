#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys

#sys.path.insert(1, os.path.join(sys.path[0], '../src/'))
import toolbox.endovir_tool
import result.mapping_result
import utils.fasta_parser

class MegahitInvestigator:

  def __init__(self):
    self.contigs = None

  def get_result(self):
    p = utils.fasta_parser.FastaParser().parse_file(self.contigs)
    return p.sequences

class EndovirModuleTool(toolbox.endovir_tool.EndovirTool):

  def __init__(self, name, path, role):
    super().__init__(name, path, role)
    self.num_threads = 4
    self.min_contig_len_nt = 300
    self.tmp_dir = '/tmp'
    self.default_options = [{'--num-cpu-threads' : self.num_threads},
                            {'--min-contig-len' : self.min_contig_len_nt},
                            {'--tmp-dir' : self.tmp_dir},
                            {'--keep-tmp-files' : None},
                            {'--continue' : None}]
    self.add_options(self.default_options)
    self.suffix = '.contigs.fa'
    self.investigator = MegahitInvestigator()

  def configure(self, settings):
    self.add_options([{'--out-dir' : settings['asmdir']}])
    self.add_options([{'--out-prefix' : settings['srr']}])
    self.investigator.contigs = os.path.join(settings['asmdir'], settings['srr']) + self.suffix

  def add_reads(self, reads):
    self.add_options([{'--read' : reads}])
