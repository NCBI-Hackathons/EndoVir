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

#sys.path.insert(1, os.path.join(sys.path[0], '../include/ncbi/src/ngs/ngs-python/'))
#from ngs import NGS
#print(sys.path, NGS)

#import screener
#import virus_contig
import status.endovir_status
import utils.endovir_utils
import toolbox.endovir_toolbox
import biodb.biodb_manager
import scanner.endovir_scanner

class Endovir:

  status_codes = status.endovir_status.EndovirStatusManager.set_status_codes(['CFGERR'])

  def __init__(self):
    self.screens = {}
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


  def scan(self, srr):
    s = scanner.endovir_scanner.EndovirScanner(self.wd, srr, 'asm')
    s.initial_scan()
    #status checkpoint

  def prepare_analysis_directory(self, srr):
    if not utils.endovir_utils.make_dir(os.path.join(self.wd, srr, 'asm')):
      sys.exit("Abort: Cannot create required analysis directories: {}".format(os.path.join(self.wd, srr, 'asm')))
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
  ev.scan(args.srr)
  return 0

if __name__ == '__main__':
  main()
