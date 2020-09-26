from mel.scripts.genclassfile.code_class import CodeClass
from mel.scripts.genclassfile.support import translate_classname

class CodeStateMachine(object):
  def __init__(self, name, states, events):
    self.files = []
    self.name = name
    machine_name = "_".join([name, 'machine'])
    machine_state_name = "_".join([machine_name, 'state'])

    var_machine_ref = translate_classname(machine_name) + "& machine"
    var_machine_state_ptr = translate_classname(machine_state_name) + "* state"

    # Machine class
    machine = CodeClass(machine_name)
    machine.add_field(translate_classname(machine_state_name), "* state_")
    (machine.add_method("void", "possible_transition", var_machine_state_ptr)
      .add_body("if(new_state) {")
      .add_body("  state_->onExit(*this);")
      .add_body("  delete state_;")
      .add_body("  state_->onEnter(*this);")
      .add_body("  state_ = new_state;")
      .add_body("}"))
    for event_name in events:
      (machine.add_method("void", event_name, var_machine_ref)
        .virtual()
        .add_body("possible_transition(state_.%s(*this));" % (event_name)))
    self.files.append(machine)

    # State base class
    machine_state = CodeClass(machine_state_name).set_virtual()
    machine_state.add_method('void', 'onEnter', var_machine_ref).virtual()
    machine_state.add_method('void', 'onExit', var_machine_ref).virtual()
    for event_name in events:
      (machine_state.add_method(translate_classname(machine_state_name) + "*", event_name, translate_classname(machine_state_name) + "& machine")
        .virtual()
        .add_body("return nullptr;"))
    self.files.append(machine_state)

    # State subclasses
    for state in states:
      state_name = "_".join([machine_state_name, state])
      state_machine = CodeClass(state_name).extend(machine_state_name)
      state_machine.add_method('void', 'onEnter', var_machine_ref).virtual()
      state_machine.add_method('void', 'onExit', var_machine_ref).virtual()

      for event_name in events:
        (state_machine.add_method(translate_classname(machine_state_name) + "*", event_name, machine_state_name + "& machine")
          .virtual()
          .add_body("return nullptr;"))
      self.files.append(state_machine)
