"""Usage: genclassfile class_name
	Generates class_name.cpp and class_name.hpp, that define interface and 
basic implementation of a class ClassName.  Note ClassName is automatically
caps munged and underscores are turned into CamelCase
"""

import os

class AlreadyExists(Exception):
  pass

class GenClassFile(object):
  def __init__(self, name, namespace):
    self.name = name.lower()
    self.header_filename = f"{self.name}.hpp"
    self.implementation_filename = f"{self.name}.cpp"
    self.namespace = namespace
    self.virtual = False
    self.extend = False

  def include_guard(self):
    return f"{self.name.upper()}_HPP"

  def classname(self):
    names = self.name.split("_")
    for i, name in enumerate(names):
      name = name.lower()
      name = name[0].upper() + name[1:]
      names[i] = name
    return ''.join(names)

  def save_header_file(self):
    if os.path.exists(self.header_filename):
        raise AlreadyExists("Header file already exists")
    with open(self.header_filename, "w") as f:
      f.write(self.header_source())

  def header_source(self):
    data = {
      'header_filename': self.header_filename,
      'classname': self.classname(),
      'namespace': self.namespace,
    }
    include_guard = self.include_guard()
    virtual = ''
    if self.virtual:
      virtual = 'virtual '
    baseclass = ''
    if self.extend:
      baseclass = f" : {self.extend}"

    return f"""#ifndef {include_guard}
#define {include_guard}

namespace { data['namespace']} {{

class {data['classname']}{baseclass} {{
  public:
    {data['classname']}();
    {virtual}~{data['classname']}();
}};

}}

#endif
"""

  def save_implementation_file(self):
    if os.path.exists(self.implementation_filename):
        raise AlreadyExists("Implementation file already exists")
    with open(self.implementation_filename, "w") as f:
      f.write(self.implementation_source())

  def implementation_source(self):
    header_filename = self.header_filename
    clsname = self.classname()
    namespace = self.namespace

    return f"""#include "{header_filename}"

using namespace {namespace};

{clsname}::{clsname}()
{{
}}

{clsname}::~{clsname}()
{{
}}
"""
