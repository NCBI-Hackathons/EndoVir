#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description A quick and dirty plugin system for endovir tools based on [0].
#
#   [0]: https://docs.python.org/3/reference/import.html
#-------------------------------------------------------------------------------
import io
import os
import sys
import importlib

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import status.endovir_status
from . import endovir_tool

class EndovirToolbox:

  status = status.endovir_status.EndovirStatusManager(status.endovir_status.EndovirStatusManager.set_status_codes(['MISSINGTOOL']))
  tools = {}
  roles = {} # Look up process by role
  modules_dir = None

  @staticmethod
  def get_module_name(toolname):
    return str(toolname+"_endovir.py")

  @staticmethod
  def isModule(modules_dir, module_name):
    return os.path.exists(os.path.join(modules_dir, module_name))

  @staticmethod
  def get_module_tool(module_name, module_dir):
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(module_dir, module_name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

  @staticmethod
  def add_tool(name, path, role, modules_dir):
    EndovirToolbox.modules_dir = modules_dir
    if name not in EndovirToolbox.tools:
      module_name = EndovirToolbox.get_module_name(name)
      if not EndovirToolbox.isModule(modules_dir, module_name):
        EndovirToolbox.tools[name] = endovir_tool.EndovirTool(name, path, role)
      else:
        module = EndovirToolbox.get_module_tool(module_name, modules_dir)
        EndovirToolbox.tools[name] = module.EndovirModuleTool(name, path, role)
      if role not in EndovirToolbox.roles:
        EndovirToolbox.roles[role] = {}
      EndovirToolbox.roles[role][name] = EndovirToolbox.tools[name]
    return EndovirToolbox.tools[name]

  @staticmethod
  def list_tools():
    for i in self.tools:
      print(self.tools[i].name)

  @staticmethod
  def get_by_name(toolname):
    return EndovirToolbox.tools.get(toolname)

  @staticmethod
  def get_by_role(role):
    return {x : EndovirToolbox.roles[role][x] for x in EndovirToolbox.roles[role]}

  @staticmethod
  def initialize_tools(tools):
    modules_dir = tools.pop('modules')
    missing_tools = {}
    for i in tools:
      for j in tools[i]:
        if not os.path.isfile(tools[i][j]):
          missing_tools[j] = tools[i][j]
        else:
          EndovirToolbox.add_tool(j, tools[i][j], i, modules_dir)
    if len(missing_tools) > 0:
      EndovirToolbox.status.set_status('MISSINGTOOL')
    return missing_tools

  @staticmethod
  def get_configurations():
    config = {'modules' : EndovirToolbox.modules_dir}
    for i in EndovirToolbox.tools:
      roles = EndovirToolbox.tools[i].get_configuration()
      for j in roles:
        if j not in config:
          config[j] = {}
        config[j].update(roles[j])
    return config

  def __init__(self):
    pass
