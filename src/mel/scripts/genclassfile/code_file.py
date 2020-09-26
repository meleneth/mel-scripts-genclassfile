import os

from mel.scripts.genclassfile.exceptions import AlreadyExists

class CodeFile(object):
  def __init__(self, target):
    self.name = target.name
    self.implementation_filename = ".".join([self.name, 'cpp'])
    self.header_filename = ".".join([self.name, 'hpp'])
    self.target = target
    self.header_includes = []
    self.implementation_includes = []
    self.namespace = None
    self.type_includes = []
    self.add_implementation_local_include(self.header_filename)
    if self.target.extend_class_name:
      self.add_header_local_include(".".join([self.target.extend_class_name, 'hpp']))
    self.add_type_include("coelacanth_types.hpp")
  def set_namespace(self, namespace):
    self.namespace = namespace
    return self
  def set_type_includes(self, type_includes):
    self.type_includes = type_includes
    return self
  def add_type_include(self, type_include):
    self.type_includes.append('"%s"' % (type_include))
    return self
  def save_header_file(self):
    if os.path.exists(self.header_filename):
        raise AlreadyExists("Header file already exists")
    with open(self.header_filename, "w") as f:
      f.write(self.header())
  def save_implementation_file(self):
    if os.path.exists(self.implementation_filename):
        raise AlreadyExists("Implementation file already exists")
    with open(self.implementation_filename, "w") as f:
      f.write(self.implementation())
  def header_filename(self):
    return ".".join([self.name, "hpp"])
  def implementation_filename(self):
    return ".".join([self.name, "cpp"])
  def add_implementation_local_include(self, name):
    self.implementation_includes.append('"%s"' % (name))
    return self
  def add_implementation_include(self, name):
    self.implementation_includes.append('<%s>' % (name))
    return self
  def add_header_local_include(self, name):
    self.header_includes.append('"%s"' % (name))
    return self
  def add_header_include(self, name):
    self.header_includes.append('<%s>' % (name))
    return self
  def header(self):
    lines = []
    lines.append("#ifndef %s" % self.include_guard())
    lines.append("#define %s" % self.include_guard())
    lines.append('')
    if len(self.header_includes):
      for header_include in self.header_includes:
        lines.append(''.join(["#include ", header_include]))
      lines.append('')
    if len(self.type_includes):
      for types_include in self.type_includes:
        lines.append(''.join(["#include ", types_include]))
      lines.append('')
    lines.append(' '.join(['namespace', self.namespace, "{"]))
    lines.append('')
    for line in self.target.declaration():
      lines.append(line)
    lines.append('')
    lines.append('}')
    lines.append('')
    lines.append('#endif')
    lines.append('')
    return "\n".join(lines)
  def implementation(self):
    lines = []
    for include in self.implementation_includes:
      lines.append(" ".join(['#include', include]))
      lines.append("")
    if self.target.extend_class_name:
      lines.append(" ".join([]))
    if self.namespace:
      lines.append("using namespace %s;" % self.namespace)
      lines.append("")
    for line in self.target.implementation():
      lines.append(line)
    return "\n".join(lines)
  def include_guard(self):
    return f"{self.name.upper()}_HPP"
