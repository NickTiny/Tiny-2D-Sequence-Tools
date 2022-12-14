from tiny_seq_tools_master.core_functions.drivers import add_driver
import bpy

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
                'pose.bones["PoseData"]["Pose"]',
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
                'pose.bones["PoseData"]["Pose Head"]',
                -1,
                f"Pose_Head/{action_length}",
            )
            new.frame_end = action_length
        return True
