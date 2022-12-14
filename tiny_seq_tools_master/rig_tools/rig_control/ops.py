import bpy


from tiny_seq_tools_master.rig_tools.rig_control.core import (
    nudge_bone,
    toggle_ik,
    change_pose,
)


class RIGCONTROL_next_body_pose(bpy.types.Operator):
    bl_idname = "rigcontrol.next_body_pose"
    bl_label = "Next Pose"
    bl_description = "Next Body Pose"

    def execute(self, context):
        return change_pose(self, context, 1, 1)


class RIGCONTROL_prev_body_pose(bpy.types.Operator):
    bl_idname = "rigcontrol.prev_body_pose"
    bl_label = "Prev Pose"
    bl_description = "Previous Body Pose"

    def execute(self, context):
        return change_pose(self, context, -1, -1)


class RIGCONTROL_next_head_pose(bpy.types.Operator):
    bl_idname = "rigcontrol.next_head_pose"
    bl_label = "Next Head"
    bl_description = "Next Head Pose"

    def execute(self, context):
        return change_pose(self, context, 0, 1)


class RIGCONTROL_prev_head_pose(bpy.types.Operator):
    bl_idname = "rigcontrol.prev_head_pose"
    bl_label = "Prev Head"
    bl_description = "Previous Head Pose"

    def execute(self, context):
        return change_pose(self, context, 0, -1)


class RIGCONTROL_r_arm_nudge_forward(bpy.types.Operator):
    bl_idname = "rigcontrol.r_arm_nudge_forward"
    bl_label = "r_arm_nudge_forward"
    bl_description = "Nudge Right Arm Towards Camera"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["R_Arm_Nudge"], False)


class RIGCONTROL_r_arm_nudge_back(bpy.types.Operator):
    bl_idname = "rigcontrol.r_arm_nudge_back"
    bl_label = "r_arm_nudge_back"
    bl_description = "Nudge Right Arm Away from Camera"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["R_Arm_Nudge"], True)


class RIGCONTROL_l_arm_nudge_forward(bpy.types.Operator):
    bl_idname = "rigcontrol.l_arm_nudge_forward"
    bl_label = "l_arm_nudge_forward"
    bl_description = "Nudge Left Arm Towards Camera"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["L_Arm_Nudge"], False)


class RIGCONTROL_l_arm_nudge_back(bpy.types.Operator):
    bl_idname = "rigcontrol.l_arm_nudge_back"
    bl_label = "l_arm_nudge_back"
    bl_description = "Nudge Left Arm Away from Camera"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["L_Arm_Nudge"], True)


class RIGCONTROL_l_leg_nudge_back(bpy.types.Operator):
    bl_idname = "rigcontrol.l_leg_nudge_back"
    bl_label = "l_leg_nudge_back"
    bl_description = "Nudge Left Leg Away from Camera"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["L_Leg_Nudge"], True)


class RIGCONTROL_l_leg_nudge_forward(bpy.types.Operator):
    bl_idname = "rigcontrol.l_leg_nudge_forward"
    bl_label = "l_leg_nudge_forward"
    bl_description = "Nudge Left Leg Towards Camera"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["L_Leg_Nudge"], False)


class RIGCONTROL_r_leg_nudge_back(bpy.types.Operator):
    bl_idname = "rigcontrol.r_leg_nudge_back"
    bl_label = "r_leg_nudge_back"
    bl_description = "Nudge Right Leg Away from Camera"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["R_Leg_Nudge"], True)


class RIGCONTROL_r_leg_nudge_forward(bpy.types.Operator):
    bl_idname = "rigcontrol.r_leg_nudge_forward"
    bl_label = "r_leg_nudge_forward"
    bl_description = "Nudge Right Leg Towards Camera"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["R_Leg_Nudge"], False)


class RIGCONTROL_toggle_ik_r(bpy.types.Operator):
    bl_idname = "rigcontrol.toggle_ik_r"
    bl_label = "R IK/FK"

    def execute(self, context):
        return toggle_ik(
            context,
            "R_Arm_IK",
        )


class RIGCONTROL_toggle_ik_l(bpy.types.Operator):
    bl_idname = "rigcontrol.toggle_ik_l"
    bl_label = "L IK/FK"

    def execute(self, context):
        return toggle_ik(
            context,
            "L_Arm_IK",
        )


class RIGCONTROL_toggle_ik_l_leg(bpy.types.Operator):
    bl_idname = "rigcontrol.toggle_ik_l_leg"
    bl_label = "L Leg IK/FK"

    def execute(self, context):
        return toggle_ik(
            context,
            "L_Leg_IK",
        )


class RIGCONTROL_toggle_ik_r_leg(bpy.types.Operator):
    bl_idname = "rigcontrol.toggle_ik_r_leg"
    bl_label = "R Leg IK/FK"

    def execute(self, context):
        return toggle_ik(
            context,
            "R_Leg_IK",
        )


classes = (
    RIGCONTROL_toggle_ik_r_leg,
    RIGCONTROL_toggle_ik_l_leg,
    RIGCONTROL_toggle_ik_l,
    RIGCONTROL_toggle_ik_r,
    RIGCONTROL_r_arm_nudge_forward,
    RIGCONTROL_r_arm_nudge_back,
    RIGCONTROL_l_arm_nudge_forward,
    RIGCONTROL_l_arm_nudge_back,
    RIGCONTROL_r_leg_nudge_forward,
    RIGCONTROL_r_leg_nudge_back,
    RIGCONTROL_l_leg_nudge_forward,
    RIGCONTROL_l_leg_nudge_back,
    RIGCONTROL_next_body_pose,
    RIGCONTROL_prev_body_pose,
    RIGCONTROL_next_head_pose,
    RIGCONTROL_prev_head_pose,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
