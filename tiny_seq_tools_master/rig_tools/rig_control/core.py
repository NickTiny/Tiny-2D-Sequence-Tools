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


def normalize_pose(pose, posemax):
    if pose in range(1, posemax + 1):
        return int(pose)
    if pose <= 0:
        return posemax
    if pose >= (posemax + 1):
        return 1


def normalize_pose_vals(datapath, offset, posemax):
    if offset == 0:
        return datapath
    pose = datapath + offset
    if pose in range(1, posemax + 1):
        return int(pose)
    if pose == 0 and offset < 0:
        return posemax
    if pose == (posemax + 1) and offset > 0:
        return 1


def change_pose(self, context, body_offset=0, head_offset=0):
    obj = context.active_object
    bone = obj.pose.bones[obj.tiny_rig.pose_data_name]
    body_val = normalize_pose_vals(
        bone["Pose"], body_offset, obj.tiny_rig.pose_length)
    head_val = normalize_pose_vals(
        bone["Pose Head"], head_offset, obj.tiny_rig.pose_length
    )
    if body_val is None or head_val is None:
        self.report({"ERROR"}, "One is none")
        return {"CANCELLED"}
    bone["Pose"] = body_val
    bone["Pose Head"] = head_val
    bone_datapath_insert_keyframe(bone, "Pose", body_val)
    bone_datapath_insert_keyframe(bone, "Pose Head", head_val)
    refresh_current_frame(context.scene)
    return {"FINISHED"}


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
            self.report(
                {"ERROR"}, f"'{bone.name}' at Z limit of {round(limit,2)}")
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
    posebone.keyframe_insert(f'["{datapath}"]', group=posebone.name)
    offset_current_frame(scene, +1)
    return


def get_bone_names(suffix):
    if "Arm" in suffix:
        return (
            f"{suffix}.Lw",
            f"{suffix}.Up",
            # f"{suffix}.Hand",
        )
    if "Leg" in suffix:
        return (
            f"{suffix}.Lw",
            f"{suffix}.Up",
            # f"{suffix}.Foot",
        )


def toggle_ik(
    context,
    datapath,
):
    bone_names = get_bone_names(datapath.split("_IK")[0])
    scene = context.scene
    index = int(scene.frame_current)
    obj = context.active_object
    posebone = obj.pose.bones[obj.tiny_rig.pose_data_name]
    ik_bone = obj.pose.bones[datapath]
    bones = [bone for bone in obj.pose.bones if bone.name in bone_names]
    if posebone[f"{datapath}"] == 1:
        save_prev_frame(scene, posebone, datapath)
        bake_constraints(bones, index)
        insert_keyframe_with_refresh(scene, posebone, datapath, 0)
        return {"FINISHED"}
    if posebone[f"{datapath}"] == 0:
        save_prev_frame(scene, posebone, datapath)
        offset_current_frame(scene, -1)
        # keyframe previous bone state
        for bone in bones:
            bone.keyframe_insert("rotation_euler", group=bone.name),
            bone.keyframe_insert("rotation_quaternion", group=bone.name)
        bake_constraints((ik_bone,), index)
        bone_matrix = ik_bone.matrix
        ik_bone.keyframe_insert("location", group=ik_bone.name)
        ik_bone.keyframe_insert("rotation_euler", group=ik_bone.name)
        offset_current_frame(scene, +1)
        reset_bones(bones)
        for bone in bones:
            bone.keyframe_insert("rotation_euler", group=bone.name)
            bone.keyframe_insert("rotation_quaternion", group=bone.name)
        insert_keyframe_with_refresh(scene, posebone, datapath, 1)
        ik_bone.matrix = bone_matrix
        ik_bone.keyframe_insert("location", group=ik_bone.name)
        ik_bone.keyframe_insert("rotation_euler", group=ik_bone.name)
        return {"FINISHED"}


def set_tiny_rig_status(obj, bool):
    obj.tiny_rig.is_rig = bool
    return obj.tiny_rig.is_rig
