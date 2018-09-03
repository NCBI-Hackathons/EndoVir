#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys

import status.endovir_status
import utils.endovir_utils
import toolbox.endovir_toolbox
import biodb.biodb_manager

class EndovirScanner:

  status_codes = status.endovir_status.EndovirStatusManager.set_status_codes(['RUNERR'])

  def __init__(self, wd, srr, asm_dir):
    self.wd = wd
    self.srr = srr
    self.asm_dir = asm_dir
    self.status = status.endovir_status.EndovirStatusManager(EndovirScanner.status_codes)

  def initial_scan(self):
    srr_mapper = toolbox.endovir_toolbox.EndovirToolbox.get_by_name('magicblast')
    srr_mapper.add_srr(self.srr)
    srr_mapper.add_database(biodb.biodb_manager.BiodbManager.get_database('refseq_virus_genomes'))
    proc = srr_mapper.assemble_process()
    #staus checkpoint
    investigator = srr_mapper.run(proc)
    print(len(investigator.mappings))
    #staus checkpoint
    #vdb_parser = s.vdbdump.run(s.srr, srr_alignments)
