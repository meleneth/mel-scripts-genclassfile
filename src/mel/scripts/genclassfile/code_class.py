from mel.scripts.genclassfile.code_method import CodeMethod
from mel.scripts.genclassfile.support import indent, translate_classname

class CodeClass(object):
  def __init__(self, name, virtual=False):
    self.name = name
    self.methods = []
    self.fields = []
    self.extend_class_name = None
    self.constructor = CodeMethod("", translate_classname(name), "")
    self.destructor = CodeMethod("", "~" + translate_classname(name), "")
    self.methods.append(self.constructor)
    self.methods.append(self.destructor)
    self._virtual = virtual

  def set_virtual(self):
    if not self._virtual:
      self._virtual = True
      self.destructor.virtual()
    return self

  def extend(self, class_name):
    self.extend_class_name = class_name
    self.set_virtual()
    return self

  def add_field(self, return_type, name):
    self.fields.append([return_type, name])
    return self

  def add_method(self, return_type, name, arguments):
    new_method = CodeMethod(return_type, name, arguments)
    self.methods.append(new_method)
    return new_method

  def declaration(self):
    lines = []
    if self.extend_class_name:
      lines.append(" ".join(['class', translate_classname(self.name),': public' , translate_classname(self.extend_class_name) , '{']))
    else:
      lines.append(" ".join(['class', translate_classname(self.name), '{']))
    lines.append(indent(['public:'])[0])
    for method in self.methods:
      lines.append(indent(indent([method.declaration()]))[0])
    for field in self.fields:
      lines.append(indent(indent([" ".join(field)]))[0])
    lines.append("};")
    return lines

  def implementation(self):
    lines = []
    for method in self.methods:
      for line in method.implementation(translate_classname(self.name)):
        lines.append(line)
    return lines
