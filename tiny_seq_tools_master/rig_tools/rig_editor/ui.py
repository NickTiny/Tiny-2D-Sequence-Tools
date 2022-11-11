import bpy


class SEQUENCER_PT_rig_editor(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_rig_edit"
    bl_label = "Tiny Rig Editor"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        obj = context.active_object
        layout = self.layout
        action_row = layout.row(align=True)

        if not (obj and obj.type == "ARMATURE"):
            return

        if obj.offset_action is not None:
            action_row.prop(context.object, "offset_action")
            if obj.library or obj.override_library:
                action_row.enabled = False

        action_row.operator("rigools.load_action", icon="FILE_REFRESH", text="")
        offset_row = layout.row(align=True)
        offset_row.operator("rigools.enable_offset_action")
        if obj.animation_data.action == obj.offset_action:
            offset_row.operator(
                "rigools.disable_offset_action", icon="LOOP_BACK", text=""
            )
        if (
            context.window_manager.offset_editor_active
            and context.active_object.mode != "POSE"
        ):
            offset_row.alert = True
            offset_row.label(text="Must be in POSE Mode")
        layout.operator("rigools.add_action_const_to_bone_head", icon="CONSTRAINT_BONE")
        layout.operator("rigools.add_action_const_to_bone", icon="CONSTRAINT_BONE")
        layout.operator("rigtools.add_ik_fk_toggle")


class SEQUENCER_PT_rig_legacy(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_rig_legacy"
    bl_label = "Update Legacy Rigs"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        self.layout.operator("rigtools.apply_legacy_transforms")
        self.layout.operator("rigools.initialize_rig")


class SEQUENCER_PT_rig_settings(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_rig_settings"
    bl_label = "Rig Settings"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        layout.label(text=f"Turnaround Length: {obj.tiny_rig.pose_length}")
        layout.operator("rigools.set_pose_length")


classes = (SEQUENCER_PT_rig_editor, SEQUENCER_PT_rig_legacy, SEQUENCER_PT_rig_settings)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
