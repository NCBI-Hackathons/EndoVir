#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \file endovir-configurator.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description Testing tool for the endovir configuration. It checks for valid
#               paths and existing tools without calling the actual screening.
#-------------------------------------------------------------------------------


import io
import os
import sys
import argparse

import configurator.endovir_configurator

def main():
  ap = argparse.ArgumentParser(description='Endovir')
  ap.add_argument('-c', '--config',
                  type=argparse.FileType('r'),
                  required=True,
                  help='endovir JSON config file')
  ap.add_argument('-f', '--fetch',
                  action='store_true',
                  help='Download databases')
  ap.add_argument('-t', '--test',
                  action='store_true',
                  help='Test configuration')
  args = ap.parse_args()
  ec = configurator.endovir_configurator.EndovirConfigurator(args.config)
  if args.test:
    ec.test()

  return 0

if __name__ == '__main__':
  main()
