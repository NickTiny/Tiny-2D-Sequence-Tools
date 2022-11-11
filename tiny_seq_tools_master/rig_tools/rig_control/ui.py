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
    l_arm_state = bone["L_Arm_IK"]
    left_col.operator(
        "rigcontrol.toggle_ik_l", text=f"IK is {boneprop_msg(l_arm_state)}"
    )
    left_col.prop(bone, '["L_Hand_Flip"]', text="Flip L Hand")
    left_col.prop(bone, '["HAND 1"]', text="L Hand")


def draw_left_leg(bone, left_col):
    left_col.label(text="L Leg")
    l_nudge_row = left_col.row(align=True)
    l_nudge_row.operator("rigcontrol.l_leg_nudge_back", icon="REMOVE", text="L")
    l_nudge_row.operator("rigcontrol.l_leg_nudge_forward", icon="ADD", text="L")
    l_arm_state = bone["L_Leg_IK"]
    left_col.operator(
        "rigcontrol.toggle_ik_l_leg", text=f"IK is {boneprop_msg(l_arm_state)}"
    )
    left_col.prop(bone, '["L_Foot_Flip"]', text="Flip L Foot")


def draw_right_arm(bone, right_col):
    right_col.label(text="R Arm")
    r_nudge_row = right_col.row(align=True)
    r_nudge_row.operator("rigcontrol.r_arm_nudge_back", icon="REMOVE", text="R")
    r_nudge_row.operator("rigcontrol.r_arm_nudge_forward", icon="ADD", text="R")
    r_arm_state = bone["R_Arm_IK"]
    right_col.operator(
        "rigcontrol.toggle_ik_r", text=f"IK is {boneprop_msg(r_arm_state)}"
    )
    right_col.prop(bone, '["R_Hand_Flip"]', text="Flip R Hand")
    right_col.prop(bone, '["HAND 2"]', text="R Hand")


def draw_right_leg(bone, right_col):
    right_col.label(text="R Leg")
    r_nudge_row = right_col.row(align=True)
    r_nudge_row.operator("rigcontrol.r_leg_nudge_back", icon="REMOVE", text="R")
    r_nudge_row.operator("rigcontrol.r_leg_nudge_forward", icon="ADD", text="R")
    r_leg_state = bone["R_Leg_IK"]
    right_col.operator(
        "rigcontrol.toggle_ik_r_leg", text=f"IK is {boneprop_msg(r_leg_state)}"
    )
    right_col.prop(bone, '["R_Foot_Flip"]', text="Flip R Foot")


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
