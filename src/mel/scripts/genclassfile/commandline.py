#!usr/bin/env python
import argparse
import logging
import sys
import os

from mel.scripts.genclassfile import CodeClass, CodeFile, CodeStateMachine

def entry_fsm(args):
  # genclassfile machine fire first_state second_state third_state
  # fire_machine
  # fire_machine_state
  # fire_machine_state_first_state
  # fire_machine_state_second_state
  # fire_machine_state_third_state
  machine = CodeStateMachine(args.name, args.states, args.events)
  for file in machine.files:
    code_file = CodeFile(file)
    code_file.set_namespace(args.namespace)
    code_file.save_header_file()
    code_file.save_implementation_file()

def entry_class(args):
  my_class = CodeClass(args.name).set_namespace(args.namespace)
  if args.extend:
    my_class.extend(args.extend)
  if args.virtual:
    my_class.virtual()
  my_file = CodeFile(my_class)
  my_file.save_header_file()
  my_file.save_implementation_file()

def get_parser():
  parser = argparse.ArgumentParser(description='generate a C++ class file')

  default_namespace = os.environ.get('classfile_namespace', 'SomeNamespace')
  parser.add_argument('--namespace','-n', help="namespace of c++ class", default=default_namespace)
  parser.add_argument('--extend','-e', help="class to extend", default=False)
  parser.add_argument('--virtual','-v', help="virtualize the destructor", action="store_true")

  subparsers = parser.add_subparsers(help='sub-command help')

  class_parser = subparsers.add_parser('class', help='')
  class_parser.set_defaults(func=entry_class)
  class_parser.add_argument('name', help="name_of_class")

  machine_parser = subparsers.add_parser('machine', help='')
  machine_parser.set_defaults(func=entry_fsm)
  machine_parser.add_argument('name', help="name_of_class")
  machine_parser.add_argument('--events', '-e', help='name of events in snake_case', nargs='*')
  machine_parser.add_argument('states', help='name of states in snake_case', nargs='*')

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
