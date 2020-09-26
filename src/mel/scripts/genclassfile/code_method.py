from mel.scripts.genclassfile.support import indent

class CodeMethod(object):
  def __init__(self, return_type, name, arguments):
    self.return_type = return_type
    self.name = name
    self.arguments = arguments
    self._virtual = False
    self.body_lines = []

  def add_body(self, line):
    self.body_lines.append(line)
    return self

  def virtual(self):
    self._virtual = True
    return self

  def declaration(self):
    return_type = ''
    if self.return_type:
      return_type = self.return_type + " "
    if self._virtual:
      return "virtual %s%s(%s);" % (return_type, self.name, self.arguments)
    return '%s%s(%s);' % (return_type, self.name, self.arguments)

  def get_return_type(self):
    if self.return_type:
      return " ".join([self.return_type, ''])
    return ''

  def get_body_lines(self):
    return indent(self.body_lines)

  def implementation(self, classname):
    results = []
    results.append("%s%s::%s(%s)" % (self.get_return_type(), classname, self.name, self.arguments))
    results.append("{")
    for line in self.get_body_lines():
      results.append(line)
    results.append("}")
    results.append("")
    return results
