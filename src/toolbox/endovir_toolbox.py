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

import tool.endovir_tool

class EndovirToolbox:

  tools = {}
  roles = {} # Look up process by role

  @staticmethod
  def add_tool(process):
    if process.name not in EndovirToolbox.tools:
      EndovirToolbox.tools[process.name] = process
      if process.role not in EndovirToolbox.roles:
        EndovirToolbox.roles[process.role] = {}
      EndovirToolbox.roles[process.role][process.name] = process
    return process

  @staticmethod
  def list_tools():
    for i in self.tools:
      print(self.tools[i].name)

  @staticmethod
  def get_by_name(toolname):
    return EndovirToolbox.tools.get(toolname)

  @staticmethod
  def get_by_role(role):
    return {x.name : x for x in EndovirToolbox.roles[role]}

  @staticmethod
  def initialize_tools(tools):
    missing_tools = {}
    for i in tools:
      for j in tools[i]:
        if not os.path.isfile(tools[i][j]):
          missing_tools[j] = tools[i][j]
        else:
          EndovirToolbox.add_tool(tool.endovir_tool.EndovirTool(j, tools[i][j], i))
    return missing_tools

  def __init__(self):
    pass
