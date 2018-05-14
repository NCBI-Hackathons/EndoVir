#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#  \file asm_base.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.1
#  \description Semi-abstract base class for assemblers.
#-------------------------------------------------------------------------------
import json

class AssemblerBase:

  def __init__(self):
    self.name = None
    self.path = None
    self.options = {}
    self.fasta_parser = parser.FastaParser()

  def load_config_file(self, cfg_file):
    fh = open(cfg_file, 'r')
    cfg = json.load(fh)
    fh.close()
    self.options = cfg.pop('options')
    self.name = cfg.pop('assembler')
    self.path = cfg.pop('path')


  def run(self, data_in, data_out):
    raise NotImplementedError("Help! Need own implementation")
