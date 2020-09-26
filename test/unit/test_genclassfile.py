import pytest

from mel.scripts.genclassfile.commandline import get_parser, entry_fsm, entry_class
from mel.scripts.genclassfile import CodeMethod, CodeFile, CodeStateMachine, CodeClass

def test_parser_parses_args():
  parser = get_parser()
  args = parser.parse_args(["class", "some_class"])
  assert args.name == "some_class"

def test_parser_parses_args_allows_namespace():
  parser = get_parser()
  args = parser.parse_args(['-n', 'MyNamespace', "class", "some_class" ])
  assert args.func == entry_class
  assert args.name == "some_class"
  assert args.namespace == "MyNamespace"

def test_parser_parses_args_machine():
  parser = get_parser()
  args = parser.parse_args(["machine", "some_class", "first_state", "second_state", "third_state"])
  assert args.func == entry_fsm
  assert args.name == "some_class"
  assert args.states == ["first_state", "second_state", "third_state"]

def test_parser_parses_args_machine_allows_event():
  parser = get_parser()
  args = parser.parse_args(["machine", "some_class", "first_state", "second_state", "third_state", "-e", "tick"])
  assert args.func == entry_fsm
  assert args.name == "some_class"
  assert args.states == ["first_state", "second_state", "third_state"]
  assert args.events == ["tick"]

def test_codemethod_declaration():
  line = CodeMethod("", "GameMachineState", "")
  assert line.declaration() == "GameMachineState();"
  assert line.implementation('GameMachineState') == [
    "GameMachineState::GameMachineState()",
    "{",
    "}",
    ""
  ]

def test_codefile_header():
  my_class = CodeClass('some_class')
  file = CodeFile(my_class).set_namespace("SuperNamespace")
  assert file.header() == """#ifndef SOME_CLASS_HPP
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



def test_implementation():
  my_class = CodeClass("some_class")
  my_file = CodeFile(my_class)
  my_file.set_namespace("SuperNamespace")

  assert my_file.implementation() == """#include "some_class.hpp"

using namespace SuperNamespace;

SomeClass::SomeClass()
{
}

SomeClass::~SomeClass()
{
}
"""

def test_header_source():
  my_class = CodeClass("some_class")
  my_file = CodeFile(my_class)
  my_file.set_namespace("SuperNamespace")

  assert my_file.header() == """#ifndef SOME_CLASS_HPP
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
  my_class = CodeClass("some_class").set_virtual()
  my_file = CodeFile(my_class)
  my_file.set_namespace("SuperNamespace")

  assert my_file.header() == """#ifndef SOME_CLASS_HPP
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
  my_class = CodeClass("some_class")
  my_class.extend("base_class")
  my_file = CodeFile(my_class)
  my_file.set_namespace("SuperNamespace")

  assert my_file.header() == """#ifndef SOME_CLASS_HPP
#define SOME_CLASS_HPP

#include "base_class.hpp"

namespace SuperNamespace {

class SomeClass : public BaseClass {
  public:
    SomeClass();
    virtual ~SomeClass();
};

}

#endif
"""

def test_code_state_machine():
  code_state_machine = CodeStateMachine("fire", ['first', 'second', 'third'], ['tick'])
  machine = code_state_machine.files[0]
  assert machine.name == "fire_machine"

  machine = code_state_machine.files[1]
  assert machine.name == "fire_machine_state"

  machine = code_state_machine.files[2]
  assert machine.name == "fire_machine_state_first"

  machine = code_state_machine.files[3]
  assert machine.name == "fire_machine_state_second"

  machine = code_state_machine.files[4]
  assert machine.name == "fire_machine_state_third"
