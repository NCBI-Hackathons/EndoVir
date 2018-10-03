#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  \ToDo: better check for continue option, e.g. something with random tmp dirs?
#-------------------------------------------------------------------------------

import io
import os
import sys

import toolbox.endovir_tool
import result.mapping_result
import bioparser.fasta.fasta_parser
import utils.sequence_container

class MegahitInvestigator:

  def __init__(self):
    self.contigs = None

  def get_result(self):
    sc = utils.sequence_container.SequenceContainer(self.contigs)
    sc.load_sequences(bioparser.fasta.fasta_parser.FastaParser())
    return sc

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

  def configure(self, options):
    self.add_options([{'--out-dir' : options['out-dir']}])
    self.add_options([{'--out-prefix' : options['out-prefix']}])
    self.add_options([{'--read' : options['read']}])
    self.investigator.contigs = os.path.join(options['out-dir'], options['out-prefix']) + self.suffix
