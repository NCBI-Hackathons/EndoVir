#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys


def make_dir(path):
  if os.path.exists(path):
    print("Found existing directory {}.".format(path))
    return True
  try:
    os.makedirs(path)
  except OSError as err:
    print("Error creating {}\t{}.".format(path, err.errno))
    return False
  return True

def isDirectory(dir_path):
  return os.path.isdir(dir_path)

def isAbsolutePath(path):
  return os.path.isabs(path)

def pathExists(path):
  return os.path.exists(path)
