import pytest

from mel.scripts.genclassfile.commandline import get_parser


def test_parser_parses_args():
  parser = get_parser()
  args = parser.parse_args(["some_class"])
  assert args.name == "some_class"

def test_parser_parses_args_allows_namespace():
  parser = get_parser()
  args = parser.parse_args(["some_class", '-n', 'MyNamespace'])
  assert args.name == "some_class"
  assert args.namespace == "some_class"
