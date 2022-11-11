import bpy

from tiny_seq_tools_master.core_functions.bone import bone_datapath_insert_keyframe
from tiny_seq_tools_master.rig_tools.rig_control.core import normalize_pose


class RIGCONTROL_settings(bpy.types.PropertyGroup):
    is_rig: bpy.props.BoolProperty(
        name="Tiny Rig Status", description="Is this Rig a Tiny Rig.", default=False
    )
    pose_length: bpy.props.IntProperty(
        name="Turnaround Length",
        description="The number of turnaround poses in this character.",
        default=0,
    )
    pose_data_name: bpy.props.StringProperty(
        name="Pose Data Bone Name", default="PoseData"
    )
    body_pose_name: bpy.props.StringProperty(name="Pose Body", default="Pose")
    head_pose_name: bpy.props.StringProperty(name="Pose Head", default="Pose Head")

    def get_body_pose(self):
        obj = self.id_data
        rig_set = obj.tiny_rig
        posedata_bone = obj.pose.bones[f"{rig_set.pose_data_name}"]
        if posedata_bone[rig_set.body_pose_name] is not None:
            return posedata_bone[rig_set.body_pose_name]
        return 0

    def set_body_pose(self, val: int):
        obj = self.id_data
        rig_set = obj.tiny_rig
        normalize_val = normalize_pose(val, rig_set.pose_length)
        normalize_head = normalize_pose(
            normalize_val + rig_set.ui_head_offset, rig_set.pose_length
        )
        bone_datapath_insert_keyframe(
            obj.pose.bones[rig_set.pose_data_name],
            rig_set.body_pose_name,
            normalize_val,
        )
        bone_datapath_insert_keyframe(
            obj.pose.bones[rig_set.pose_data_name],
            rig_set.head_pose_name,
            normalize_head,
        )

        return

    iu_body_pose: bpy.props.IntProperty(
        name="Body Pose",
        get=get_body_pose,
        set=set_body_pose,
        options=set(),
        min=1,
        max=20,
    )

    def get_head_pose(self):
        obj = self.id_data
        rig_set = obj.tiny_rig
        posedata_bone = obj.pose.bones[f"{rig_set.pose_data_name}"]
        if (
            posedata_bone[rig_set.body_pose_name]
            and posedata_bone[rig_set.head_pose_name]
        ):
            if posedata_bone[rig_set.head_pose_name] != 0:
                return (
                    posedata_bone[rig_set.head_pose_name]
                    - posedata_bone[rig_set.body_pose_name]
                )
        return 0

    def set_head_pose(self, val: int):
        obj = self.id_data
        rig_set = obj.tiny_rig
        posedata_bone = obj.pose.bones[f"{rig_set.pose_data_name}"]
        if val == 0:  # if no offset set head pose to body pose
            bone_datapath_insert_keyframe(
                obj.pose.bones[rig_set.pose_data_name],
                rig_set.head_pose_name,
                posedata_bone[rig_set.body_pose_name],
            )
            return
        normalize_val = (
            val + posedata_bone[rig_set.body_pose_name]
        ) % rig_set.pose_length

        normalize_val = normalize_pose(normalize_val, rig_set.pose_length)
        bone_datapath_insert_keyframe(
            obj.pose.bones[rig_set.pose_data_name],
            rig_set.head_pose_name,
            normalize_val,
        )
        return

    ui_head_offset: bpy.props.IntProperty(
        name="Head Offset",
        get=get_head_pose,
        set=set_head_pose,
        options=set(),
        min=-20,
        max=20,
    )


classes = (RIGCONTROL_settings,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.offset_action = bpy.props.PointerProperty(
        name="Offset Action", type=bpy.types.Action
    )
    bpy.types.Object.tiny_rig = bpy.props.PointerProperty(type=RIGCONTROL_settings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.offset_action
    del bpy.types.Object.tiny_rig
