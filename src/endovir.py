#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  endovir.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


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

import utils.endovir_utils
import toolbox.endovir_toolbox
import biodb.biodb_manager


class Endovir:

  class Config:

    def __init__(self, config):
      self.wd = config.pop('wd')
      if not os.path.isabs(self.wd):
        self.wd = os.path.join(os.getcwd(), self.wd)
      utils.endovir_utils.make_dir(self.wd)
      self.dbdir = os.path.join(self.wd, config.pop('dbdirectory'))
      utils.endovir_utils.make_dir(self.dbdir)
      self.flank_len = config.pop('flank_length')

  def __init__(self, config_file):
    config = json.load(config_file)
    self.config = self.Config(config['analysis'])
    self.toolbox = toolbox.endovir_toolbox.EndovirToolbox()
    self.toolbox.configure(config['tools'])
    self.dbmanager = biodb.biodb_manager.BiodbManager(self.toolbox)
    self.dbmanager.configure(self.config.dbdir, config['databases'])
    self.dbmanager.test_databases()
    self.screens = {}

  # def initial_screen():
  #   return contigs
  # def analyze_contigs():
  #
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
  ap.add_argument('-srr', type=str, default='SRR5150787',
                  help='SRR number, e.g. SRR5150787'),
  ap.add_argument('-c', '--config', type=argparse.FileType('r'),
                  help='endovir JSON config file')
  args = ap.parse_args()

  #srrs = ['SRR5150787', 'SRR5832142']
  #if args.srr == 'SRR5150787':
    #print("Running test in {} using {}".format(args.wd, args.srr), file=sys.stderr)
  #else:
    #print("Analyzing  {} using {}.".format(args.srr, args.wd), file=sys.stderr)
  ev = Endovir(args.config)
  #e = Endovir(wd=args.wd)
  #print("Checking databases", file=sys.stderr)
  #e.setup()
  #print("Starting screen", file=sys.stderr)
  #e.screen([args.srr])
  return 0

if __name__ == '__main__':
  main()
