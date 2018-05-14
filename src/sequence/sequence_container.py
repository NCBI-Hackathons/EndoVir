#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  -------------------------------------------------------------------------------
#  \file sequence_container.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description Class managing sequences
#  -------------------------------------------------------------------------------

import io
import os
import sys

from . import sequence

class SequenceContainer:

  def __init__(self):
    self.sequences = {}
    self.size = 0

  def add_sequence(self, sequence):
    if sequence.name != None:
      self.sequence[sequence.name] = sequence
      self.size += 1
    else:
      print("Warning: skipped empty sequence")
