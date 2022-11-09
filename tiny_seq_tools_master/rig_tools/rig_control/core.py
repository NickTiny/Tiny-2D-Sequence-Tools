import bpy


from tiny_seq_tools_master.core_functions.bone import (
    bake_constraints,
    reset_bones,
    get_consts_on_bone,
    bone_datapath_insert_keyframe,
)
from tiny_seq_tools_master.core_functions.scene import (
    refresh_current_frame,
    offset_current_frame,
)

pbone_name = "PoseData"


def get_nudge_limits(bone):
    for const in get_consts_on_bone(bone, "LIMIT_LOCATION"):
        if abs(const.min_z) == abs(const.max_z):
            return abs(const.max_z) * -1


def nudge_bone(self, bone, negative):
    val = 0.05
    if negative:
        val = -0.05

    # Check bone is at limits
    limit = get_nudge_limits(bone)
    if limit is not None:
        if negative:
            limit = abs(limit)
        if (bone.location[2] <= limit and not negative) or (
            bone.location[2] >= limit and negative
        ):
            self.report({"ERROR"}, f"'{bone.name}' at Z limit of {round(limit,2)}")
            return {"CANCELLED"}

    bone.location[2] += -val
    bone.keyframe_insert("location")
    return {"FINISHED"}


def insert_keyframe_with_refresh(
    scene, posebone: bpy.types.PoseBone, datapath: str, val: int
):
    bone_datapath_insert_keyframe(posebone, datapath, val)
    refresh_current_frame(scene)
    return


def save_prev_frame(scene, posebone: bpy.types.PoseBone, datapath: str):
    offset_current_frame(scene, -1)
    posebone.keyframe_insert(f'["{datapath}"]')
    offset_current_frame(scene, +1)
    return


def toggle_ik(context, datapath, bone_names, ik_bone_names):
    scene = context.scene
    index = int(scene.frame_current)
    obj = context.active_object
    posebone = obj.pose.bones[pbone_name]

    bones = [bone for bone in obj.pose.bones if bone.name in bone_names]
    ik_bones = [bone for bone in obj.pose.bones if bone.name in ik_bone_names]
    if posebone[f"{datapath}"] == 1:
        save_prev_frame(scene, posebone, datapath)
        bake_constraints(bones, ik_bones, index)
        insert_keyframe_with_refresh(scene, posebone, datapath, 0)
        return {"FINISHED"}
    if posebone[f"{datapath}"] == 0:
        save_prev_frame(scene, posebone, datapath)
        offset_current_frame(scene, -1)
        # keyframe previous bone state
        for bone in bones:
            bone.keyframe_insert("rotation_euler")
            bone.keyframe_insert("rotation_quaternion")
        offset_current_frame(scene, +1)
        reset_bones(bones)
        for bone in bones:
            bone.keyframe_insert("rotation_euler")
            bone.keyframe_insert("rotation_quaternion")
        insert_keyframe_with_refresh(scene, posebone, datapath, 1)
        return {"FINISHED"}