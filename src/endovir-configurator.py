#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \file endovir-configurator.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Testing tool for the endovir configuration. It checks for valid
#               paths and existing tools without calling the actual screening.
#-------------------------------------------------------------------------------


import io
import os
import sys
import argparse

import configurator.endovir_configurator

def main():
  ap = argparse.ArgumentParser(description='Endovir configurator')
  ap.add_argument('-c', '--config',
                  type=argparse.FileType('r'),
                  required=True,
                  help='endovir JSON config file')
  ap.add_argument('-i', '--install',
                  action='store_true',
                  help='Download and install databases')
  ap.add_argument('-t', '--test',
                  action='store_true',
                  help='Test configuration')
  ap.add_argument('-e', '--email',
                  type=str,
                  help='Email required by NCBI Eutils')
  ap.add_argument('-p', '--prepare',
                  action='store_true',
                  help='Prepare configuration for endovir screen')
  args = ap.parse_args()
  ec = configurator.endovir_configurator.EndovirConfigurator(args.config)
  if args.test:
    ec.test()
    return 0
  if args.install:
    ec.install_databases(args.email)
    return 0
  if args.prepare:
    ec.prepare()
    return 0
  return 0

if __name__ == '__main__':
  main()
