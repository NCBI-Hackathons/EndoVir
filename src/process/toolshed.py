#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  -------------------------------------------------------------------------------
#  \file toolshed.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys


class EndovirToolshed:

  def __init__(self):
    self.tool_map = {}
    self.role_map = {} # Look up process by role

  def add_tool(self, process):
    self.tool_map[process.name] = process
    if process.role not in self.role_map:
      self.role_map[process.role] = {}
    self.role_map[process.role][process.name] = process

  def list_tools(self):
    for i in self.tool_map:
      print(self.tool_map[i].name)

  def get_tool_by_name(self, toolname):
    return self.tool_map.get(toolname)

  def get_role_tools(self, role):
    return {x.name : x for x in self.roles[role]}
