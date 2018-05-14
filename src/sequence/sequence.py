#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#  \file sequence.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description Implementation of a biological sequence.
#-------------------------------------------------------------------------------

import io
import os
import sys

class Sequence:

  def __init__(self, name=None, sequence=None, description=None):
    self.name = name
    self.sequence = seqence
    self.length = None
    if sequence != None:
      self.length = len(seqence)
    self.description = None
