#-------------------------------------------------------------------------------
#  \file endovir_configurator.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Configuration for endovir. Databses require external tools and
#               therefore tools need to be initiaized first.
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

  def get_flank_length(self):
    return self.config['analysis']['flank_length']

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
    print("Found all required tools", file=sys.stderr)

  def configure_databases(self):
    dbmanager = biodb.biodb_manager.BiodbManager(self.get_working_directory())
    dbmanager.initialize_databases(self.get_databases())
    dbmanager.test_databases()

  def install_databases(self, email):
    missing_tools = toolbox.endovir_toolbox.EndovirToolbox.initialize_tools(self.get_tools())
    dbmanager = biodb.biodb_manager.BiodbManager(self.get_working_directory())
    dbmanager.install_databases(self.get_databases(), email)

  def prepare(self):
    self.configure_toolbox()
    self.configure_databases()
    config = {'analysis' : {'wd' : os.path.abspath(self.get_working_directory()),
                            'flank_length' : self.get_flank_length()}}
    #config = {}
    config['databases'] = biodb.biodb_manager.BiodbManager.get_configurations()
    config['tools'] = toolbox.endovir_toolbox.EndovirToolbox.get_configurations()
    print(json.dumps(config))
