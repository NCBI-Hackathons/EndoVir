#-------------------------------------------------------------------------------
#  \file endovir_configurator.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Configuration for endovir. Databses require external tools and
#               therefore tools need to be initialized first.
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging

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
    self.configure_working_directory()
    self.configure_toolbox()
    self.configure_databases()

  def configure_toolbox(self):
    missing_tools = toolbox.endovir_toolbox.EndovirToolbox.initialize_tools(self.get_tools())
    if len(missing_tools) != 0:
      print("Following tools cannot been found:")
      for i in missing_tools:
        print("{}\t{}".format(i, missing_tools[i]))
      sys.exit("Please install or adjust paths. Abort")
    print("Found all required tools", file=sys.stderr)

  def configure_databases(self):
    biodb.biodb_manager.BiodbManager.initialize_databases(self.get_working_directory(),
                                                          self.get_databases())
    biodb.biodb_manager.BiodbManager.test_databases()

  def install_databases(self, email):
    missing_tools = toolbox.endovir_toolbox.EndovirToolbox.initialize_tools(self.get_tools())
    biodb.biodb_manager.BiodbManager.install_databases(self.get_working_directory(),
                                                       self.get_databases(),
                                                       email)

  def configure_working_directory(self):
    if not utils.endovir_utils.isDirectory(self.get_working_directory()):
      if not utils.endovir_utils.makedir(self.get_working_directory()):
        sys.exit("Cannot create working directory: {}.Abort".format(self.get_working_directory()))
      print("Created working directory {}".format(self.get_working_directory()), file=sys.stderr)
    else:
      print("Found working directory {}".format(self.get_working_directory()), file=sys.stderr)

  def prepare(self):
    self.configure_toolbox()
    self.configure_databases()
    config = {
                'analysis' :
                {
                  'wd' : os.path.abspath(self.get_working_directory()),
                  'flank_length' : self.get_flank_length()
                }
             }
    config['databases'] = biodb.biodb_manager.BiodbManager.get_configurations()
    config['tools'] = toolbox.endovir_toolbox.EndovirToolbox.get_configurations()
    print(json.dumps(config))
