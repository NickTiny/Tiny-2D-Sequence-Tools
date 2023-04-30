import bpy
from tiny_seq_tools_master.core_functions.bone import get_consts_on_bone
from tiny_seq_tools_master.core_functions.drivers import get_driver_ob_obj, add_driver
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
    armature_mod = get_gpencil_armature_modifier(obj)
    if armature_mod:
        return enable_mod_rig_gpencil(obj, bool)
    armature_constraint = get_armature_constraint(obj)
    if armature_constraint:
        return enable_cont_rig_gpencil(obj, bool)


def armature_bones_rename(armature: bpy.types.Armature, bone_legend: dict):
    """bone_legend must be in {'old_name': 'new_name',} format"""
    updated_bones = ""
    for bone in armature.bones:
        if bone.name in bone_legend:
            updated_bones += f"{bone.name},"
            bone.name = bone_legend[bone.name]

    return f"Bones Renamed: {updated_bones} \n"


def bone_custom_prop_bools_add(bone: bpy.types.PoseBone, bools_to_add):
    """bools_to_add should be a = ['str', 'str', 'str',]"""
    for index, item in enumerate(bools_to_add):
        custom_int_create(bone, bools_to_add[index], 1, 0, 1)

def custom_int_create_timeoffset(target, name, value, min, max):
    custom_int_create(target, name, value, min, max)
    target.id_data.tiny_rig.user_props += name

def custom_int_create(target, name, value, min, max):
    target[name] = value
    id_props = target.id_properties_ui(name)
    id_props.update(
        min=min,
        max=max,
        default=1,
    )
    target.property_overridable_library_set(f'["{name}"]', True)
    return target[name]


def bone_create_groups(obj: bpy.types.Object, bone_groups: dict):
    """bone_groups must be in {'name': color_set',} format"""
    status = False
    for key, value in bone_groups.items():
        try:
            obj.pose.bone_groups[key]
        except KeyError:
            group = obj.pose.bone_groups.new(name=key)
            group.color_set = value
            status = True
    return status


def bone_assign_groups(obj: bpy.types.Object, bone_assignments: dict):
    """bone_assignments must be in {'bone_name': group_name',} format"""
    updated_bones = ""
    for bone in obj.pose.bones:
        if bone.name in bone_assignments:
            bone.bone_group = obj.pose.bone_groups[bone_assignments[bone.name]]
            updated_bones += f"{bone.name},"
    obj.data.show_group_colors = True
    if updated_bones != "":
        updated_bones = f"Changed Bone Group: {updated_bones}"
    return updated_bones


def bone_transform_mirror_add(bone, name="FLIP_BONE"):
    """bone must be hand or foot bone"""
    prefix = bone.name[0]
    suffix = bone.name.split(".")[1]
    new = bone.constraints.new("TRANSFORM")
    new.name = name
    new.target = bone.id_data
    new.subtarget = f"{bone.name.split('.')[0]}_Nudge"
    new.target_space = "LOCAL_WITH_PARENT"
    new.owner_space = "LOCAL_WITH_PARENT"
    new.map_to = "ROTATION"
    new.to_min_y_rot = 3.1415927410125732
    add_driver(
        bone.id_data,
        bone.id_data,
        f"{prefix}_{suffix}_Flip",
        f'pose.bones["{bone.name}"].constraints["{new.name}"].influence',
        f'pose.bones["{bone.id_data.tiny_rig.pose_data_name}"]["{prefix}_{suffix}_Flip"]',
    )


def bone_transform_nudge_add(bone, name="HAND_NUDGE"):
    """Bone must be a hand or Foot"""
    suffix = bone.name.split(".Hand")[0]
    side = suffix.split("_Arm")[0]
    constraint = bone.constraints.new("TRANSFORM")
    constraint.target = bone.id_data
    constraint.subtarget = f"{suffix}_Nudge"
    constraint.target_space = "LOCAL"
    constraint.owner_space = "LOCAL"
    constraint.to_min_z = -0.05
    constraint.name = name
    add_driver(
        bone.id_data,
        bone.id_data,
        f"{side}_Hand_Nudge",
        f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
        f'pose.bones["{bone.id_data.tiny_rig.pose_data_name}"]["{side}_Hand_Nudge"]',
    )
    return constraint


def bone_copy_location_limb(context, bone, driver=True, name="COPY_LIMB_LOC"):
    """Copy location of Lw bone to IK Target bone"""
    prefix = bone.name[0]
    suffix = bone.name[2:5]
    mod_type = "COPY_LOCATION"
    constraint = bone.constraints.new(mod_type)
    constraint.name = name
    constraint.target = bone.id_data
    constraint.subtarget = f"{prefix}_{suffix}.Lw"
    constraint.target_space = "POSE"
    constraint.owner_space = "POSE"
    constraint.head_tail = 1.0
    constraint.use_bbone_shape = False
    constraint.use_x = True
    constraint.use_y = False
    constraint.use_z = True

    if driver:
        expression = f"{bone.name} == 0"
        add_driver(
            bone.id_data,
            bone.id_data,
            bone.name,
            f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
            f'pose.bones["{context.scene.bone_selection}"]["{bone.name}"]',
            -1,
            expression,
        )
    return constraint


def add_ik_flip_to_pole(bone, nudge_bone_name, name="IK_FLIP"):
    constraint = bone.constraints.new("TRANSFORM")
    constraint.name = name
    constraint.target = bone.id_data
    constraint.subtarget = nudge_bone_name
    constraint.target_space = "LOCAL"
    constraint.owner_space = "LOCAL"
    constraint.to_min_y = -4.5
    return constraint


def get_nudge_bone_name(bone):
    prefix = bone.name[0]
    suffix = bone.name[2:5]
    return f"{prefix}_{suffix}_Nudge"


def copy_ik_rotation(bone, target_name, name="COPY_IK_ROT"):
    mod_type = "COPY_ROTATION"
    constraint = bone.constraints.new(mod_type)
    constraint.name = name
    constraint.target = bone.id_data

    constraint.subtarget = target_name


def bone_copy_location_nudge(bone, space="POSE", offset=False, name="COPY_NUDGE_LOC"):
    """Copy Location from Limb's 'Nudge' Bone"""
    nudge_bone_name = get_nudge_bone_name(bone)
    mod_type = "COPY_LOCATION"
    constraint = bone.constraints.new(mod_type)
    constraint.name = name
    constraint.target = bone.id_data
    constraint.subtarget = nudge_bone_name
    constraint.target_space = space
    constraint.owner_space = space
    constraint.head_tail = 0.0
    constraint.use_bbone_shape = False
    constraint.use_x = False
    constraint.use_y = True
    constraint.use_z = False
    constraint.use_offset = offset
    return constraint


def bone_ik_driver_add(bone, constraint, propbone, ik_prop_name):
    """Add Driver to IK's Influence"""
    custom_int_create(propbone, ik_prop_name, 1, 0, 1)
    add_driver(
        bone.id_data,
        bone.id_data,
        ik_prop_name,
        f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
        f'pose.bones["{propbone.name}"]["{ik_prop_name}"]',
        -1,
    )
    return


def bone_ik_constraint_add(bone, prefix, suffix):
    """Add IK Constrain on Lw Bone, with Target + Pole"""
    # angle = (0 if bone.name(".").split[0] else 180)
    constraint = bone.constraints.new("IK")
    constraint.target = bone.id_data
    constraint.subtarget = f"{prefix}_{suffix}_IK"
    constraint.pole_target = bone.id_data
    constraint.pole_subtarget = f"{prefix}_{suffix}_Pole"
    # constraint.pole_angle = angle
    constraint.chain_count = 2
    constraint.use_tail = True
    return constraint


def bone_position_limits_add(bone, name="Nudge - Limit Location"):
    """Position Limits on Limb's 'Nudge' Bone"""
    suffix = bone.name.split(".Hand")[0]
    side = suffix.split("_Arm")[0]
    constraint = bone.constraints.new("LIMIT_LOCATION")
    constraint.owner_space = "LOCAL"
    constraint.use_min_z = True
    constraint.use_max_z = True
    constraint.min_z = -0.1
    constraint.max_z = 0.1
    constraint.name = name
    return constraint


def bone_check_constraint(bone, name):
    constraint_names = [item.name for item in bone.constraints]
    return name in constraint_names


def bone_copy_transforms_add(bone, name):
    """Only Add to Eyelid/Brow Bones"""
    constraint = bone.constraints.new("COPY_TRANSFORMS")
    constraint.name = name
    constraint.target = bone.id_data
    constraint.subtarget = f"{bone.name}.001"
    constraint.head_tail = 0.0
    constraint.use_bbone_shape = False
    constraint.target_space = "LOCAL"
    constraint.owner_space = "LOCAL"


def bone_copy_location_add(bone, subtarget, offset, name):
    """Only Add to Eye Bones"""
    constraint = bone.constraints.new("COPY_LOCATION")
    constraint.name = name
    constraint.target = bone.id_data
    constraint.subtarget = subtarget
    constraint.use_offset = offset
    constraint.target_space = "LOCAL"
    constraint.owner_space = "LOCAL"