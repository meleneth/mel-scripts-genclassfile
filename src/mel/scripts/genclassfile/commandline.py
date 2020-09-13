#!usr/bin/env python
import argparse
import logging
import sys
import os

from mel.scripts.genclassfile import GenClassFile

def entry_default(args):
  gen = GenClassFile(args.name, args.namespace)
  gen.virtual = args.virtual
  gen.extend = args.extend
  gen.save_header_file()
  gen.save_implementation_file()

def get_parser():
  parser = argparse.ArgumentParser(description='generate a C++ class file')
  parser.set_defaults(func=entry_default)
  parser.add_argument('name', help="name_of_class")
  default_namespace = os.environ.get('genclassfile_namespace', 'SomeNamespace')
  parser.add_argument('--namespace','-n', help="namespace of c++ class", default=default_namespace)
  parser.add_argument('--extend','-e', help="class to extend", default=False)
  parser.add_argument('--virtual','-v', help="virtualize the destructor", default=False)
  return parser

def main():
  logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
    stream=sys.stdout)
  logger = logging.getLogger()

  parser = get_parser()
  args = parser.parse_args()
  args.func(args)

