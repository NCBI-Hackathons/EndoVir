#-------------------------------------------------------------------------------
#  \file endovir_configurator.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description Cconfiguration for endovir.
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging


#sys.path.insert(1, os.path.join(sys.path[0], '../include/ncbi/src/ngs/ngs-python/'))
#from ngs import NGS
#print(sys.path, NGS)

#import screener
#import virus_contig

import utils.endovir_utils
import toolbox.endovir_toolbox
import biodb.biodb_manager


class EndovirConfigurator:

  def __init__(self, config_file):
    self.config = json.load(config_file)

  def get_tools(self):
      return self.config['tools']

  def get_working_directory(self):
    return self.config['analysis']['wd']

  def get_databases(self):
    return self.config['databases']

  def test(self):
    self.configure_toolbox()
    self.configure_databases()

  def configure_toolbox(self):
    missing_tools = toolbox.endovir_toolbox.EndovirToolbox().initialize_tools(self.get_tools())
    if len(missing_tools) != 0:
      print("Following tools cannot been found:")
      for i in missing_tools:
        print("{}\t{}".format(i, missing_tools[i]))
      sys.exit("Please install or adjust paths. Abort")
    print("Found all required tools")

  def configure_databases(self):
    dbmanager = biodb.biodb_manager.BiodbManager(self.get_working_directory())
    dbmanager.initialize_databases(self.get_databases())
    dbmanager.test_databases()

  def install_databases(self):
    missing_tools = toolbox.endovir_toolbox.EndovirToolbox().initialize_tools(self.get_tools())
    dbmanager = biodb.biodb_manager.BiodbManager(self.get_working_directory())
    dbmanager.install_databases(self.get_databases())
