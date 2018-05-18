"""
-------------------------------------------------------------------------------
\file untitled.py
\author Jan P Buchmann <jan.buchmann@sydney.edu.au>
\copyright 2018 The University of Sydney
\version 0.0.0
\description
-------------------------------------------------------------------------------
"""
import io
import os
import sys


def make_dir(path):
  if os.path.exists(path):
    print("Found existing direcotry {}.".format(path))
    return True
  try:
    os.mkdir(path)
  except OSError as err:
    print("Error creating {}\t{}.".format(path, err.errno))
    return False
  return True
