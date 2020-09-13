import pytest

from mel.scripts.genclassfile.commandline import get_parser
from mel.scripts.genclassfile import GenClassFile


def test_parser_parses_args():
  parser = get_parser()
  args = parser.parse_args(["some_class"])
  assert args.name == "some_class"

def test_parser_parses_args_allows_namespace():
  parser = get_parser()
  args = parser.parse_args(["some_class", '-n', 'MyNamespace'])
  assert args.name == "some_class"
  assert args.namespace == "MyNamespace"


def test_implementation_source():
  gen = GenClassFile("some_class", "SuperNamespace")
  assert gen.implementation_source() == """#include "some_class.hpp"

using namespace SuperNamespace;

SomeClass::SomeClass()
{
}

SomeClass::~SomeClass()
{
}
"""

def test_header_source():
  gen = GenClassFile("some_class", "SuperNamespace")
  assert gen.header_source() == """#ifndef SOME_CLASS_HPP
#define SOME_CLASS_HPP

namespace SuperNamespace {

class SomeClass {
  public:
    SomeClass();
    ~SomeClass();
};

}

#endif
"""

def test_header_source_virtual():
  gen = GenClassFile("some_class", "SuperNamespace")
  gen.virtual = True
  assert gen.header_source() == """#ifndef SOME_CLASS_HPP
#define SOME_CLASS_HPP

namespace SuperNamespace {

class SomeClass {
  public:
    SomeClass();
    virtual ~SomeClass();
};

}

#endif
"""

def test_header_source_extend():
  gen = GenClassFile("some_class", "SuperNamespace")
  gen.extend = "BaseClass"
  assert gen.header_source() == """#ifndef SOME_CLASS_HPP
#define SOME_CLASS_HPP

namespace SuperNamespace {

class SomeClass : BaseClass {
  public:
    SomeClass();
    ~SomeClass();
};

}

#endif
"""
