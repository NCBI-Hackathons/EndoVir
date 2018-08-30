#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------
import io
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import status.endovir_status
from . import endovir_tool

class EndovirToolbox:

  status = status.endovir_status.EndovirStatusManager(status.endovir_status.EndovirStatusManager.set_status_codes(['MISSINGTOOL']))
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
          EndovirToolbox.add_tool(endovir_tool.EndovirTool(j, tools[i][j], i))
    if len(missing_tools) > 0:
      EndovirToolbox.status.set_status('MISSINGTOOL')
    return missing_tools

  @staticmethod
  def get_configurations():
    config = {}
    for i in EndovirToolbox.tools:
      roles = EndovirToolbox.tools[i].get_configuration()
      for j in roles:
        if j not in config:
          config[j] = {}
        config[j].update(roles[j])
    return config

  def __init__(self):
    pass
