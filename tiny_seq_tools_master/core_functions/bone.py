from tiny_seq_tools_master.core_functions.drivers import add_driver
import bpy
import math
import numpy as np
# PoseBone


def select_bones(bones):
    bpy.ops.pose.select_all(action="DESELECT")
    for bone in bones:
        bone.bone.select = True
    return


def reset_bones(bones):
    for n in bones:
        n.location = (0, 0, 0)
        n.rotation_quaternion = (1, 0, 0, 0)
        n.rotation_axis_angle = (0, 0, 1, 0)
        n.rotation_euler = (0, 0, 0)


def reset_all_bone_transformations(obj):
    bpy.ops.pose.select_all(action="SELECT")
    bpy.ops.pose.loc_clear()
    bpy.ops.pose.select_all(action="DESELECT")


def bone_datapath_insert_keyframe(
    posebone: bpy.types.PoseBone,
    datapath: str,
    val: int,
    frame=None,
    index=-1,
):
    group = posebone.name
    if frame is None:
        frame = bpy.context.scene.frame_current
    posebone[f"{datapath}"] = val
    return posebone.keyframe_insert(
        f'["{datapath}"]', index=index, frame=frame, group=group
    )


# Constraint
def get_consts_on_bone(bone, type) -> list:
    return [constraint for constraint in bone.constraints if constraint.type == type]


def show_hide_constraints(list, bool):
    for const in list:
        const.enabled = bool


def set_cons_state(bones, type, bool):
    for bone in bones:
        for constraint in get_consts_on_bone(bone, type):
            constraint.enabled = bool


def get_consts_on_bone(bone: bpy.types.PoseBone, type) -> list:
    return [constraint for constraint in bone.constraints if constraint.type == type]


def show_hide_constraints(list, bool):
    for const in list:
        const.enabled = bool


def apply_transforms_on_frame(index, bones):
    bpy.ops.pose.loc_clear()
    set_cons_state(bones, "TRANSFORM", True)
    bpy.context.scene.frame_set(index)
    bpy.ops.nla.bake(
        frame_start=index,
        frame_end=index,
        step=1,
        only_selected=True,
        visual_keying=True,
        clear_constraints=False,
        clear_parents=False,
        use_current_action=True,
        clean_curves=True,
        bake_types={"POSE"},
    )
    set_cons_state(bones, "TRANSFORM", False)


def bake_constraints(bones, index):
    select_bones(bones)
    bpy.ops.nla.bake(
        frame_start=index,
        frame_end=index,
        step=1,
        only_selected=True,
        visual_keying=True,
        clear_constraints=False,
        clear_parents=False,
        use_current_action=True,
        clean_curves=False,
        bake_types={"POSE"},
    )
    return


def add_action_const_to_body(context):
    action_length = int(context.active_object.offset_action.frame_range[1])
    for bone in context.selected_pose_bones:
        if not get_consts_on_bone(bone, "ACTION"):
            new = bone.constraints.new("ACTION")
            new.action = bone.id_data.offset_action
            new.use_eval_time = True
            add_driver(
                bone.id_data,
                bone.id_data,
                "Pose",
                f'pose.bones["{bone.name}"].constraints["{new.name}"].eval_time',
                f'pose.bones["{bone.id_data.tiny_rig.pose_data_name}"]["Pose"]',
                -1,
                f"Pose/{action_length}",
            )
            new.frame_end = action_length
        return


def add_action_const_to_head(context):
    action_length = int(context.active_object.offset_action.frame_range[1])
    for bone in context.selected_pose_bones:
        if not get_consts_on_bone(bone, "ACTION"):
            new = bone.constraints.new("ACTION")
            new.action = bone.id_data.offset_action
            new.use_eval_time = True
            add_driver(
                bone.id_data,
                bone.id_data,
                "Pose_Head",
                f'pose.bones["{bone.name}"].constraints["{new.name}"].eval_time',
                f'pose.bones["{bone.id_data.tiny_rig.pose_data_name}"]["Pose Head"]',
                -1,
                f"Pose_Head/{action_length}",
            )
            new.frame_end = action_length
        return True

def bone_new(
    edit_bones,
    name: str,
    head,
    tail,
    global_y=0,
):
    bone = edit_bones.new(name)
    # a new bone will have zero length and not be kept
    # move the head/tail to keep the bone
    bone.head = (head[0], global_y, head[1])
    bone.tail = (tail[0], global_y, tail[1])
    return bone

def child_bone_new(
    parent_bone: bpy.types.EditBone,
    name: str,
    head,
    tail,
):

    bone = bone_new(parent_bone.id_data.edit_bones, name, head, tail)
    bone.parent = parent_bone
    return bone


def child_bone_connected_new(
    parent_bone: bpy.types.EditBone,
    name: str,
    tail,
):
    head = parent_bone.tail.xz
    bone = bone_new(parent_bone.id_data.edit_bones, name, head, tail)
    bone.parent = parent_bone
    bone.use_connect = True
    return bone


def make_nudge(parent_bone, prefix, limb, up_limb_head):
    new_head = (up_limb_head[0], up_limb_head[1]+.1)
    tail = (new_head[0]-.1, new_head[1])
    return child_bone_new(parent_bone, f'{prefix}_{limb}_Nudge', new_head, tail)


def make_limb(parent_bone: bpy.types.EditBone, prefix: str, limb: str, origin, angle: int, appendage_angle: int,):
    limb_up = child_bone_new(
        parent_bone, f'{prefix}_{limb}.Up', origin, calculate_bone_vector(.6, origin, angle))
    limb_lw = child_bone_connected_new(
        limb_up, f'{prefix}_{limb}.Lw', calculate_bone_vector(.7, limb_up.tail.xz, angle*.98))
    limb_appendage = child_bone_connected_new(
        limb_lw, f'{prefix}_{limb}.{get_appendage_name(limb)}', calculate_bone_vector(.2, limb_lw.tail.xz, appendage_angle))
    return [limb_up, limb_lw, limb_appendage]


def calculate_bone_vector(length, origin, angle=0):
    x = length * math.sin(math.radians(angle)) + origin[0]
    y = length * math.cos(math.radians(angle)) + origin[1]
    return (x, y)

def calculate_bone_angle(p2, p1):
    return math.degrees(math.atan2((p2[0]-p1[0]), (p2[1]-p1[1])))


def make_nudge_bone(nudge_parent, prefix: str, limb: str, origin,):
    new_head = (origin[0], origin[1]+.1)
    tail = (new_head[0]-.1, new_head[1])
    return child_bone_new(nudge_parent, f'{prefix}_{limb}_Nudge', new_head, tail)

def get_appendage_name(limb):
    if limb == "Leg":
        return "Foot"
    if limb == "Arm":
        return "Hand"

def make_limb_chain(parent_bone: bpy.types.EditBone, prefix: str, limb: str, origin, angle: int, appendage_angle: int, use_make_nudge=True, use_make_iks=True, use_mirror=False):
    angle_mirror = 1
    if use_mirror:
        angle_mirror = -1
    angle = angle*angle_mirror
    appendage_angle = appendage_angle*angle_mirror

    if use_make_nudge:
        parent_bone = make_nudge_bone(parent_bone, prefix, limb, origin)
    limbs = make_limb(parent_bone, prefix, limb,
                      origin, angle, appendage_angle)
    return limbs


def make_limb_set(parent, limb, origin, angle: int, appendage_angle: int, use_make_nudge=True, make_ik_bones=True):
    r_limbs = make_limb_chain(parent_bone=parent, prefix='R', limb=limb, origin=origin, angle=angle,
                              appendage_angle=appendage_angle, use_make_nudge=use_make_nudge, use_make_iks=make_ik_bones, use_mirror=False)
    l_limbs = make_limb_chain(
        parent, 'L', limb, [-origin[0], origin[1]], angle, appendage_angle, use_make_nudge=use_make_nudge, use_make_iks=make_ik_bones, use_mirror=True)


def make_ik_bones(parent_bone: bpy.types.PoseBone, limb_bone, use_mirror=False):
    prefix = limb_bone.name[0]
    limb = limb_bone.name[2:5]
    root_bone = parent_bone
    mirror_mult = (1 if prefix == "R" else -1)
    if limb == "Leg":
        root_bone = parent_bone.id_data.edit_bones[0]

    limb_angle = calculate_bone_angle(
        (limb_bone.tail.xz[0], limb_bone.tail.xz[1]), (limb_bone.head.xz[0], limb_bone.head.xz[1]))

    ik_offset = calculate_bone_vector(
        1, (limb_bone.head.xz[0], limb_bone.head.xz[1]), (limb_angle))
    
    ik_bone = child_bone_new(
        root_bone, f"{prefix}_{limb}_IK", ik_offset, calculate_bone_vector(.2, ik_offset,   limb_angle))

    pole_offset = calculate_bone_vector(
        2, (limb_bone.head.xz[0], limb_bone.head.xz[1]), (limb_angle+(90*mirror_mult)))
    pole_bone = child_bone_new(
        parent_bone, f"{prefix}_{limb}_Pole", pole_offset, calculate_bone_vector(.2, pole_offset, (limb_angle+(90*mirror_mult))))
    return [ik_bone, pole_bone]
