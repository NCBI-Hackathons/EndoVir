#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  -------------------------------------------------------------------------------
#  \file endovir_configurator.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#  -------------------------------------------------------------------------------

import io
import os
import sys
import json
import argparse

from . import database_configurator
from . import tools_configurator

class EndovirConfigurator:

  def __init__(self):
    pass

  def configure(self, cfg_file, ev_config):
    config = json.load(cfg_file)
    ev_config.flank_len = config['analysis'].get('flank_length')
    toolshed = self.config_tools(config.get('tools'))
    ev_config.wd = self.config_wd(config['analysis'].get('wd'))
    self.config_dbs(ev_config, config.get('databases'), toolshed)

  def config_tools(self, tools):
    tcf = tools_configurator.ToolsConfigurator()
    tcf.config(tools)

  def config_dbs(self, ev_config, dbs, toolshed):
    ev_config.dbdir = os.path.join(ev_config.wd, dbs['direcotry'])
    self.create_database_directory(ev_config.dbdir)
    dbc = database_configurator.DatabaseConfigurator()
    dbc.config(dbs, self.config.dbdir, toolshed)

  def create_working_directory(self, ev_wd):
    if not os.path.isdir(ev_wd):
      if not self.make_dir(ev_wd):
        print("Cannot create working directory {}.Abort.".format(ev_wd))
        sys.exit()
      print("Working directory is: {}".format(ev_wd))

  def create_database_directory(self, dbdir):
    if not os.path.isdir(self.config.dbdir):
      if not self.make_dir(self.config.dbdir):
        print("Cannot create database directory {}.Abort.".format(self.config.dbdir))
        sys.exit()
      print("Database directory is: {}".format(self.config.dbdir))

  def config_wd(self, wd):
    ev_wd = wd if os.path.isabs(wd) else os.path.join(os.getcwd(), wd)
    self.create_working_directory(ev_wd)
    return ev_wd

  def make_dir(self, path):
    try:
      os.mkdir(path)
    except OSError as err:
      print("Error creating {}\t{}.".format(path, err.errno))
      return False
    return True
