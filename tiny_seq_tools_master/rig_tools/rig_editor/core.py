import bpy
from tiny_seq_tools_master.core_functions.bone import get_consts_on_bone
from tiny_seq_tools_master.core_functions.drivers import get_driver_ob_obj
from tiny_seq_tools_master.core_functions.object import get_consts_on_obj

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


def enable_all_mod_const(obj, bool):
    for mod in obj.grease_pencil_modifiers:
        mod.show_viewport = bool
    for const in obj.constraints:
        const.enabled = bool


def get_grease_pencil_modifiers(obj, type):
    return [mod for mod in obj.grease_pencil_modifiers if mod.type == type]


def gpencil_fix_offset_show_viewport(obj: bpy.types.Object, bool: bool):
    mods = get_grease_pencil_modifiers(obj, "GP_TIME")
    for mod in [mod for mod in mods if mod.mode == "FIX"]:
        mod.show_viewport = bool


def get_armature_constraint(obj) -> bpy.types.Constraint:
    constraints = get_consts_on_obj(obj, "ARMATURE")
    if len(constraints) == 1:
        return constraints[0]


def enable_rig(rig, bool):
    position = "POSE"
    if bool == False:
        position = "REST"
    rig.data.pose_position = position


def enable_lattice_mod(obj, bool):
    for mod in get_grease_pencil_modifiers(obj, "GP_LATTICE"):
        mod.show_viewport = bool


def get_gpencil_armature_modifier(obj):
    mods = get_grease_pencil_modifiers(obj, "GP_ARMATURE")
    if len(mods) == 1:
        return mods[0]


def enable_gpencil_armature_modifier(mod, bool):
    rig = mod.object
    enable_rig(rig, bool)
    mod.show_viewport = bool


def enable_armature_constraint(const, bool):
    const.enabled = bool
    rig = const.targets[0].target
    enable_rig(rig, bool)
    return True


def enable_cont_rig_gpencil(obj, bool):
    # Check Driver on GP
    if len(get_driver_ob_obj(obj)) != 1:
        return False
    armature_constraint = get_armature_constraint(obj)
    # Reset Rig
    enable_armature_constraint(armature_constraint, bool)
    # Disable Time Offset Modifiers
    gpencil_fix_offset_show_viewport(obj, bool)
    enable_lattice_mod(obj, bool)


def enable_mod_rig_gpencil(obj, bool):
    armature_mod = get_gpencil_armature_modifier(obj)
    # Reset Rig
    enable_gpencil_armature_modifier(armature_mod, bool)
    # Disable Time Offset Modifiers
    gpencil_fix_offset_show_viewport(obj, bool)
    enable_lattice_mod(obj, bool)
    return True


def hide_grease_pencil_editor(obj, bool):
    # Check Driver on GP
    if len(get_driver_ob_obj(obj)) != 1:
        return False
    armature_mod = get_gpencil_armature_modifier(obj)
    if armature_mod:
        return enable_mod_rig_gpencil(obj, bool)
    armature_constraint = get_armature_constraint(obj)
    if armature_constraint:
        return enable_cont_rig_gpencil(obj, bool)
