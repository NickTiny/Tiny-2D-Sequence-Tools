import bpy


from tiny_seq_tools_master.rig_tools.rig_control.core import nudge_bone, toggle_ik


class RIGCONTROL_r_arm_nudge_forward(bpy.types.Operator):
    bl_idname = "rigcontrol.r_arm_nudge_forward"
    bl_label = "r_arm_nudge_forward"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["R_Arm_Nudge"], False)


class RIGCONTROL_r_arm_nudge_back(bpy.types.Operator):
    bl_idname = "rigcontrol.r_arm_nudge_back"
    bl_label = "r_arm_nudge_back"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["R_Arm_Nudge"], True)


class RIGCONTROL_l_arm_nudge_forward(bpy.types.Operator):
    bl_idname = "rigcontrol.l_arm_nudge_forward"
    bl_label = "l_arm_nudge_forward"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["L_Arm_Nudge"], False)


class RIGCONTROL_l_arm_nudge_back(bpy.types.Operator):
    bl_idname = "rigcontrol.l_arm_nudge_back"
    bl_label = "l_arm_nudge_back"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["L_Arm_Nudge"], True)


class RIGCONTROL_l_leg_nudge_back(bpy.types.Operator):
    bl_idname = "rigcontrol.l_leg_nudge_back"
    bl_label = "l_leg_nudge_back"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["L_Leg_Nudge"], True)


class RIGCONTROL_l_leg_nudge_forward(bpy.types.Operator):
    bl_idname = "rigcontrol.l_leg_nudge_forward"
    bl_label = "l_leg_nudge_forward"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["L_Leg_Nudge"], False)


class RIGCONTROL_r_leg_nudge_back(bpy.types.Operator):
    bl_idname = "rigcontrol.r_leg_nudge_back"
    bl_label = "r_leg_nudge_back"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["R_Leg_Nudge"], True)


class RIGCONTROL_r_leg_nudge_forward(bpy.types.Operator):
    bl_idname = "rigcontrol.r_leg_nudge_forward"
    bl_label = "r_leg_nudge_forward"

    def execute(self, context):
        return nudge_bone(self, context.active_object.pose.bones["R_Leg_Nudge"], False)


class RIGCONTROL_toggle_ik_r(bpy.types.Operator):
    bl_idname = "rigcontrol.toggle_ik_r"
    bl_label = "R IK/FK"

    def execute(self, context):
        return toggle_ik(
            context,
            "R_Arm_IK",
            ("R_Arm.Lw", "R_Arm.Up", "R_Arm.Hand"),
            ("R_Arm_IK", "R_Arm_Pole"),
        )


class RIGCONTROL_toggle_ik_l(bpy.types.Operator):
    bl_idname = "rigcontrol.toggle_ik_l"
    bl_label = "L IK/FK"

    def execute(self, context):
        return toggle_ik(
            context,
            "L_Arm_IK",
            ("L_Arm.Lw", "L_Arm.Up", "L_Arm.Hand"),
            ("L_Arm_IK", "L_Arm_Pole"),
        )


class RIGCONTROL_toggle_ik_l_leg(bpy.types.Operator):
    bl_idname = "rigcontrol.toggle_ik_l_leg"
    bl_label = "L Leg IK/FK"

    def execute(self, context):
        return toggle_ik(
            context,
            "L_Leg_IK",
            ("L_Leg.Lw", "L_Leg.Up", "L_Leg.Foot"),
            ("L_Leg_IK", "L_Leg_Pole"),
        )


class RIGCONTROL_toggle_ik_r_leg(bpy.types.Operator):
    bl_idname = "rigcontrol.toggle_ik_r_leg"
    bl_label = "R Leg IK/FK"

    def execute(self, context):
        return toggle_ik(
            context,
            "R_Leg_IK",
            ("R_Leg.Lw", "R_Leg.Up", "R_Leg.Foot"),
            ("R_Leg_IK", "R_Leg_Pole"),
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
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
