from tiny_seq_tools_master.core_functions.bone import get_consts_on_bone


# Action Constraints
def get_action_offset_bones(bones):
    action_constraints = []
    for bone in bones:
        for const in get_consts_on_bone(bone, "ACTION"):
            action_constraints.append(const)
    return action_constraints


def get_action_from_constraints(bones):
    actions = []
    for bone in bones:
        for const in get_consts_on_bone(bone, "ACTION"):
            if const.action not in actions:
                actions.append(const.action)
    # There should only be one action on action constraints for tiny rigs
    if len(actions) != 1:
        return
    return actions[0]
