import bpy


def check_tiny_rig(obj):
    if obj.type != "ARMATURE":
        return
    try:
        return obj.pose.bones[obj.tiny_rig.pose_data_name] or obj.pose.bones[obj.tiny_rig.pose_data_name]["L_Arm_IK"]
    except KeyError:
        return


def draw_arm(bone, col, side, limb):
    if bone.id_data.tiny_rig.is_ik:
        draw_nudge_row(col, side, limb)
        draw_ik_row(col, side, limb)
    sub_limb = get_sub_limb(limb)
    col.separator()
    hand_row = col.row(align=True)
    if bone.id_data.tiny_rig.is_ik:
        hand_row.prop(
            bpy.context.window_manager.tiny_rig_ui,
            f"{side}_Hand_Nudge",
            icon="SORT_DESC",
            text="",
        )
    hand_row.prop(bone, f'["{side}_Hand"]', text=f"{side} Hand")
    hand_row.prop(
        bpy.context.window_manager.tiny_rig_ui,
        f"{side}_{sub_limb}_Mirror",
        icon="MOD_MIRROR",
        text="",
    )


def get_sub_limb(limb):
    sub_limb = "Foot"
    if limb == "Arm":
        sub_limb = "Hand"
    return sub_limb


def draw_leg(bone, col, side, limb):
    if bone.id_data.tiny_rig.is_ik:
        draw_nudge_row(col, side, limb)
        draw_ik_row(col, side, limb)
    sub_limb = get_sub_limb(limb)
    col.prop(
        bpy.context.window_manager.tiny_rig_ui,
        f"{side}_{sub_limb}_Mirror",
        icon="MOD_MIRROR",
        text=f"Mirror {side} {sub_limb}",
    )


def draw_nudge_row(col, side, limb):
    col.label(text=f"{side} {limb}")
    nudge_row = col.row(align=True)
    nudge_row.operator(
        f"rigcontrol.{side.lower()}_{limb.lower()}_nudge_back",
        icon="REMOVE",
        text=f"{side} Back",
    )
    nudge_row.operator(
        f"rigcontrol.{side.lower()}_{limb.lower()}_nudge_forward",
        icon="ADD",
        text=f"{side} Forward",
    )


def draw_ik_row(col, side, limb):
    ik_row = col.row(align=True)
    ik_row.prop(
        bpy.context.window_manager.tiny_rig_ui,
        f"{side}_{limb}_IK",
        icon="CON_KINEMATIC",
        text=f"{side} {limb} IK",
    )
    ik_row.prop(
        bpy.context.window_manager.tiny_rig_ui,
        f"{side}_{limb}_Flip_IK",
        icon="CON_ROTLIKE",
        text="",
    )


def draw_limb_control(bone, col):
    row = col.row()
    split = row.split(factor=0.5)
    left_col = split.column(align=True)
    draw_arm(bone, left_col, "L", "Arm")
    draw_leg(bone, left_col, "L", "Leg")
    right_col = split.split()
    right_col = right_col.column(align=True)
    draw_arm(bone, right_col, "R", "Arm")
    draw_leg(bone, right_col, "R", "Leg")


def draw_pose_row(layout, bone, body):
    pose_row = layout.row(align=True)
    pose_row.operator(f"rigcontrol.prev_{body}_pose", icon="BACK", text="")
    pose_row.prop(bone.id_data.tiny_rig, f"ui_{body}_pose")
    pose_row.operator(f"rigcontrol.next_{body}_pose", icon="FORWARD", text="")


def draw_brow_row(layout, bone):
    brow_row = layout.row(align=False)
    brow_row.prop(bone, '["A. Brow L"]', text="Left Brow")
    brow_row.prop(bone, '["A. Brow R"]', text="Right Brow")


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
        if not obj.tiny_rig.is_rig:
            return
        layout = self.layout
        if not check_tiny_rig(obj):
            layout.label(text="Rig not Found", icon="ERROR")
            return
        bone = obj.pose.bones[obj.tiny_rig.pose_data_name]

        

        draw_brow_row(layout, bone)

        layout.separator()

        if bone.get('A. Mouth') is not None:
            layout.prop(bone, '["A. Mouth"]', text="Mouth")

        if bone.get('A. Hat') is not None:
            layout.prop(bone, '["A. Hat"]', text="Hat")

        if bone.id_data.tiny_rig.is_turnaround:
            draw_pose_row(layout, bone, "head")
            draw_pose_row(layout, bone, "body")

        for x in bone.keys():
            if x in obj.tiny_rig.user_props and not (x == "L_Hand" or x == "R_Hand"):
                layout.prop(bone, f'["{x}"]')

        layout.separator()

        col = layout.column()
        draw_limb_control(bone, col)


classes = (SEQUENCER_PT_rig_control,)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
