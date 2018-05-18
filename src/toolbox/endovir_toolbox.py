#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  -------------------------------------------------------------------------------
#  \file endovir_toolbox.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#  -------------------------------------------------------------------------------
import io
import os
import sys

import endovir_tool.endovir_tool

class EndovirToolbox:

  def __init__(self):
    self.tools_map = {}
    self.roles_map = {} # Look up process by role

  def add_tool(self, process):
    self.tools_map[process.name] = process
    if process.role not in self.roles_map:
      self.roles_map[process.role] = {}
    self.roles_map[process.role][process.name] = process

  def list_tools(self):
    for i in self.tools_map:
      print(self.tools_map[i].name)

  def get_tool_by_name(self, toolname):
    return self.tools_map.get(toolname)

  def get_tools_by_role(self, role):
    return {x.name : x for x in self.roles[role]}

  def configure(self, config):
    missing_tools = self.initialize_tools(config)
    if len(missing_tools) != 0:
      print("Following tools cannot been found:")
      for i in missing_tools:
        print("{}\t{}".format(i, missing_tools[i]))
      sys.exit("Please install or adust paths. Abort")
    print("Found all required tools and put them into the endovir toolbox")

  def initialize_tools(self, tools):
    missing_tools = {}
    for i in tools:
      for j in tools[i]:
        if not os.path.isfile(tools[i][j]):
          missing_tools[j] = tools[i][j]
        else:
          self.add_tool(endovir_tool.endovir_tool.EndovirTool(j, tools[i][j], i))
    return missing_tools
