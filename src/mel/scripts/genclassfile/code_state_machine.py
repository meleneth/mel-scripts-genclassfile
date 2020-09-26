from mel.scripts.genclassfile.code_class import CodeClass
from mel.scripts.genclassfile.support import translate_classname

class CodeStateMachine(object):
  def __init__(self, name, states, events):
    self.files = []
    self.name = name
    machine_name = "_".join([name, 'machine'])
    machine_state_name = "_".join([machine_name, 'state'])
    machine_state_ptr = translate_classname(machine_state_name) + "*"
    machine_class_name = translate_classname(machine_name)

    var_machine_ref = machine_class_name + "& machine"
    var_machine_state_ptr = machine_state_ptr + " state"

    machine = CodeClass(machine_name)
    machine.add_field(machine_state_ptr, "state_")
    machine.add_method("void", "possible_transition", var_machine_state_ptr)
    machine.add_method(machine_state_ptr, "tick", var_machine_ref).virtual()
    self.files.append(machine)
    machine_state = CodeClass(machine_state_name).set_virtual()
    machine_state.add_method('void', 'onEnter', var_machine_ref).virtual()
    machine_state.add_method('void', 'onExit', var_machine_ref).virtual()

    self.files.append(machine_state)
    for state in states:
      state_name = "_".join([machine_state_name, state])
      state_machine = CodeClass(state_name).extend(machine_state_name)
      state_machine.add_method('void', 'onEnter', var_machine_ref).virtual()
      state_machine.add_method('void', 'onExit', var_machine_ref).virtual()
      state_machine.add_method(machine_state_ptr, "tick", var_machine_ref).virtual()

      for event_name in events:
        (state_machine.add_method(machine_state_ptr, event_name, machine_state_name + "& machine")
          .add_body("return nullptr;"))
      self.files.append(CodeClass(state_name).extend(machine_state_name))
