import bpy


def boneprop_msg(prop):
    if prop == 1:
        return "ON"
    else:
        return "OFF"


def check_tiny_rig(obj):
    if obj.type != "ARMATURE":
        return
    try:
        return obj.pose.bones["PoseData"] or obj.pose.bones["PoseData"]["L_Arm_IK"]
    except KeyError:
        return


def draw_left_arm(bone, left_col):
    left_col.label(text="L Arm")
    l_nudge_row = left_col.row(align=True)
    l_nudge_row.operator("rigcontrol.l_arm_nudge_back", icon="REMOVE", text="L")
    l_nudge_row.operator("rigcontrol.l_arm_nudge_forward", icon="ADD", text="L")

    ik_row_l = left_col.row(align=True)
    ik_row_l.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "L_Arm_IK",
        icon="CON_KINEMATIC",
        text="L Arm IK",
    )
    ik_row_l.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "L_Arm_Flip_IK",
        icon="MOD_MIRROR",
        text="",
    )
    left_col.separator()
    L_Handrow = left_col.row(align=True)
    L_Handrow.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "L_Hand_Nudge",
        icon="SORT_DESC",
        text="",
    )
    L_Handrow.prop(bone, '["HAND 1"]', text="L Hand")
    L_Handrow.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "L_Hand_Mirror",
        icon="MOD_MIRROR",
        text="",
    )


def draw_left_leg(bone, left_col):
    left_col.label(text="L Leg")
    l_nudge_row = left_col.row(align=True)
    l_nudge_row.operator("rigcontrol.l_leg_nudge_back", icon="REMOVE", text="L")
    l_nudge_row.operator("rigcontrol.l_leg_nudge_forward", icon="ADD", text="L")
    ik_row_l = left_col.row(align=True)
    ik_row_l.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "L_Leg_IK",
        icon="CON_KINEMATIC",
        text="L Leg IK",
    )
    ik_row_l.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "L_Leg_Flip_IK",
        icon="MOD_MIRROR",
        text="",
    )

    left_col.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "L_Foot_Mirror",
        icon="MOD_MIRROR",
        text="L Foot",
    )


def draw_right_arm(bone, right_col):
    right_col.label(text="R Arm")
    R_nudge_row = right_col.row(align=True)
    R_nudge_row.operator("rigcontrol.r_arm_nudge_back", icon="REMOVE", text="R")
    R_nudge_row.operator("rigcontrol.r_arm_nudge_forward", icon="ADD", text="R")
    ik_row_r = right_col.row(align=True)
    ik_row_r.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "R_Arm_IK",
        icon="CON_KINEMATIC",
        text="R Arm IK",
    )
    ik_row_r.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "R_Arm_Flip_IK",
        icon="MOD_MIRROR",
        text="",
    )
    right_col.separator()
    R_handrow = right_col.row(align=True)
    R_handrow.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "R_Hand_Nudge",
        icon="SORT_DESC",
        text="",
    )
    R_handrow.prop(bone, '["HAND 2"]', text="R Hand")
    R_handrow.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "R_Hand_Mirror",
        icon="MOD_MIRROR",
        text="",
    )


def draw_right_leg(bone, right_col):
    right_col.label(text="R Leg")
    R_nudge_row = right_col.row(align=True)
    R_nudge_row.operator("rigcontrol.r_leg_nudge_back", icon="REMOVE", text="R")
    R_nudge_row.operator("rigcontrol.r_leg_nudge_forward", icon="ADD", text="R")
    ik_row_r = right_col.row(align=True)
    ik_row_r.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "R_Leg_IK",
        icon="CON_KINEMATIC",
        text="R Leg IK",
    )
    ik_row_r.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "R_Leg_Flip_IK",
        icon="MOD_MIRROR",
        text="",
    )

    right_col.prop(
        bpy.context.window_manager.tiny_rig_ui,
        "R_Foot_Mirror",
        icon="MOD_MIRROR",
        text="R Foot",
    )


def draw_limb_control(bone, col):
    row = col.row()
    split = row.split(factor=0.5)
    left_col = split.column(align=True)
    draw_left_arm(bone, left_col)
    draw_left_leg(bone, left_col)
    right_col = split.split()
    right_col = right_col.column(align=True)
    draw_right_arm(bone, right_col)
    draw_right_leg(bone, right_col)


class SEQUENCER_PT_rig_control(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_rig_control"
    bl_label = "Tiny Rig Controller"
    bl_category = "Tiny Rig Control"

    def draw(self, context):

        obj = context.active_object
        if obj is None:
            return
        # if not obj.tiny_rig_is_rig:
        #     return
        layout = self.layout
        if not check_tiny_rig(obj):
            layout.label(text="Rig not Found", icon="ERROR")
            return
        bone = obj.pose.bones["PoseData"]

        head_row = layout.row(align=True)
        head_row.operator("rigcontrol.prev_head_pose", icon="BACK", text="")
        head_row.prop(bone.id_data.tiny_rig, "ui_head_offset")
        head_row.operator("rigcontrol.next_head_pose", icon="FORWARD", text="")

        pose_row = layout.row(align=True)
        pose_row.operator("rigcontrol.prev_body_pose", icon="BACK", text="")
        pose_row.prop(bone.id_data.tiny_rig, "ui_body_pose")
        pose_row.operator("rigcontrol.next_body_pose", icon="FORWARD", text="")

        layout.prop(bone, '["A. Mouth"]', text="Mouth")
        col = layout.column()
        draw_limb_control(bone, col)


classes = (SEQUENCER_PT_rig_control,)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
