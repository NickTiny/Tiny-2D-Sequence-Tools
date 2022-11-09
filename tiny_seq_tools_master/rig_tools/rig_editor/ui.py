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

        if obj.type != "ARMATURE":
            return

        if context.object.offset_action is not None:
            action_row.prop(context.object, "offset_action")
        action_row.operator("rigools.load_action", icon="FILE_REFRESH", text="")
        offset_row = layout.row(align=True)
        offset_row.operator("rigools.enable_offset_action")
        if obj.animation_data.action == obj.offset_action:
            offset_row.operator(
                "rigools.disable_offset_action", icon="LOOP_BACK", text=""
            )
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


classes = (SEQUENCER_PT_rig_editor, SEQUENCER_PT_rig_legacy)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
