#!/usr/bin/python3
#-------------------------------------------------------------------------------
# \author Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
# \copyright 2017,2018 The University of Sydney
# \description
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '.'))

import status.endovir_status
import utils.endovir_utils
import toolbox.endovir_toolbox
import biodb.biodb_manager
import scanner.endovir_scanner

class Endovir:

  status_codes = status.endovir_status.EndovirStatusManager.set_status_codes(['CFGERR'])

  class EndovirScreen:

    def __init__(self, srr, wd, assembly_dir, contigs_dir, virus_db, prot_db):
      self.srr = srr
      self.wd = wd
      self.asm_dir = os.path.join(wd, srr, assembly_dir)
      self.virus_db = virus_db
      self.prot_db = prot_db
      self.ctg_dir = os.path.join(wd, srr, contigs_dir)
      self.flank_len = 500

  def __init__(self):
    self.screen = None
    self.wd = None
    self.flank_len = None
    self.status = status.endovir_status.EndovirStatusManager(Endovir.status_codes)

  def load_configuration(self, config_file):
    if config_file == None:
      self.parse_configuration(json.load(sys.stdin))
    else:
      fh = open(config_file, 'r')
      self.parse_configuration(json.load(fh))
      fh.close()

  def parse_configuration(self, config):
    self.wd = config['analysis']['wd']
    self.flank_len = config['analysis']['flank_length']
    toolbox.endovir_toolbox.EndovirToolbox.initialize_tools(config['tools'])
    biodb.biodb_manager.BiodbManager.initialize_databases(self.wd, config['databases'])

  def scan(self):
    s = scanner.endovir_scanner.EndovirScanner(self.screen)
    s.initial_scan(mapper='magicblast', assembler='megahit', contig_screener='blastx')
    #s.bud(mapper='magicblast')
    #status checkpoint

  def prepare_analysis_directory(self, srr, assembly_dir='asm', contigs_dir='ctgs'):
    self.screen = self.EndovirScreen(srr,
                                     self.wd,
                                     assembly_dir,
                                     contigs_dir,
                                     'refseq_virus_genomes',
                                     'virus_refseq_proteins')
    for i in [self.screen.asm_dir, self.screen.ctg_dir]:
      if not utils.endovir_utils.make_dir(i):
        sys.exit("Abort: Cannot create required analysis directory: {}".format(i))
    print("Endovir  is GO", file=sys.stderr)

  #def screen(self, srrs=[]):
    #vrs_ctgs = {}
    #for i in srrs:
      #print("Screening {0}".format(i), file=sys.stderr)
      #s = screener.Screener(self.wd, i, self.dbs['virusdb'], self.dbs['cdd'])
      #srr_alignments = s.screen_srr(s.srr, s.virus_db.path)
      #vdb_parser = s.vdbdump.run(s.srr, srr_alignments)
      #contigs = s.assemble(vdb_parser.dump_to_file())
      #putative_virus_contigs = s.cdd_screen(contigs, s.cdd_db.path, os.path.join(s.wd, 'rpst'))
      #if len(putative_virus_contigs) > 0:
        #for j in putative_virus_contigs:
          #c = virus_contig.VirusContig("ctg_"+str(len(vrs_ctgs)),
                                      #s.assembler.parser.sequences[j].sequence,
                                      #i,
                                      #s.assembler.parser.sequences[j].header,
                                      #self.flank_len,
                                      #s.wd)
          #vrs_ctgs[c.name] = c
          #print("Prepared {} for budding".format(c.name))
        #print("Budding {} contigs".format(len(vrs_ctgs)))
        #s.bud(vrs_ctgs)
      #else:
        #print("No contigs with virus motifs detected")
        #sys.exit()

def main():
  ap = argparse.ArgumentParser(description='Endovir')
  ap.add_argument('-srr',
                  type=str,
                  default='SRR5150787',
                  help='SRR accession, e.g. SRR5150787'),
  ap.add_argument('-c', '--config',
                  type=str,
                  default=None,
                  help='endovir JSON config file')
  args = ap.parse_args()

  ev = Endovir()
  ev.load_configuration(args.config)
  ev.prepare_analysis_directory(args.srr)
  ev.scan()
  return 0

if __name__ == '__main__':
  main()
