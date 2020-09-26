def indent(lines, spaces="  "):
  return [''.join([spaces, line]) for line in lines]

def translate_classname(name):
  names = name.split("_")
  for i, name in enumerate(names):
    name = name.lower()
    name = name[0].upper() + name[1:]
    names[i] = name
  return ''.join(names)
