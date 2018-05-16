#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  -------------------------------------------------------------------------------
#  \file tools_configurator.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#  -------------------------------------------------------------------------------
import os
import sys
import process.toolshed
import process.basic_process

class ToolsConfigurator:

  def __init__(self):
    self.toolshed = process.toolshed.EndovirToolshed()

  def config(self, tools):
    missing_tools = self.check_tool_paths(tools)
    if len(missing_tools) > 0:
      print("Following tools cannot been found:")
      for i in missing_tools:
        print("{}\t{}".format(i, missing_tools[i]))
      sys.exit("Please install or adust paths. Abort")
    print("Found all required tools and put them into the endovir toolshed")
    return self.toolshed

  def check_tool_paths(self, tools):
    missing_tools = {}
    for i in tools:
      for j in tools[i]:
        if not os.path.isfile(tools[i][j]):
          missing_tools[j] = tools[i][j]
        else:
          self.toolshed.add_tool(process.basic_process.BasicProcess(j, tools[i][j], i))
    return missing_tools
