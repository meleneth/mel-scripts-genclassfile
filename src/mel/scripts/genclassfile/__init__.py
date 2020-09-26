"""Usage: genclassfile class_name
	Generates class_name.cpp and class_name.hpp, that define interface and
basic implementation of a class ClassName.  Note ClassName is automatically
caps munged and underscores are turned into CamelCase
"""

from mel.scripts.genclassfile.code_method import CodeMethod
from mel.scripts.genclassfile.code_class import CodeClass
from mel.scripts.genclassfile.code_file import CodeFile
from mel.scripts.genclassfile.code_state_machine import CodeStateMachine
from mel.scripts.genclassfile.exceptions import AlreadyExists

# FIXME - look up to the .git file
# load the .genclassfile at the same dir level as .git
