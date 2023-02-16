import bpy

from tiny_seq_tools_master.core_functions.drivers import get_driver_ob_obj


class SEQUENCER_PT_turnaround_editor(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_turnaround_editor"
    bl_label = "Turnaround Editor"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        obj = context.active_object
        layout = self.layout
        action_row = layout.row(align=True)
        if not obj.tiny_rig.is_rig:
            self.layout.label(text="Rig not Found", icon="ARMATURE_DATA")
            return

        action_row.prop(context.object, "offset_action")
        if obj.offset_action is not None:
            
            if obj.library or obj.override_library:
                action_row.enabled = False

        action_row.operator("rigools.load_action", icon="FILE_REFRESH", text="")
        offset_row = layout.row(align=True)
        offset_row.operator("rigools.enable_offset_action", icon="ACTION_TWEAK")
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
        layout.operator("rigools.add_action_const_to_bone", icon="CONSTRAINT_BONE")


class SEQUENCER_PT_driver_editor(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_driver_editor"
    bl_label = "Edit Bone Drivers"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        if not context.active_object.tiny_rig.is_rig:
            self.layout.label(text="Rig not Found", icon="ARMATURE_DATA")
            return
        layout = self.layout
        layout.operator(
            "rigtools.add_ik_fk_toggle",
            icon="CON_KINEMATIC",
            text="Add Driver to Existing IK",
        )
        layout.operator("rigools.add_ik_mirror_to_pole", icon="CON_ROTLIKE")
        layout.operator("rigools.add_hand_nudge", icon="SORT_DESC")
        layout.operator(
            "rigools.add_mirror_to_hand_foot_bone",
            text="Add Mirror to Hand/Foot",
            icon="MOD_MIRROR",
        )


class SEQUENCER_PT_rig_grease_pencil(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_rig_grease_pencil"
    bl_label = "Rigged Grease Pencil Editor"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        self.layout.operator("rigools.enable_all_gp_mod_const", icon="CHECKMARK")
        edit_gp_row = self.layout.row(align=True)
        edit_gp_row.operator("rigools.enter_grease_pencil_editor", icon="GREASEPENCIL")
        if context.window_manager.gpencil_editor_active:
            obj_row = self.layout.row()
            obj_row.enabled = False
            obj_row.prop(
                context.window_manager, "gpencil_editor_active", text="Active GP"
            )
            edit_gp_row.operator(
                "rigools.enter_grease_pencil_editor_exit", icon="LOOP_BACK", text=""
            )
            drivers = get_driver_ob_obj(context.active_object)
            self.layout.label(
                text=f"Currently Editing {drivers[0].driver.expression}: {context.scene.frame_current}"
            )
        row = self.layout.row(align=True)
        row.operator("rigools.isolate_gpencil", icon="HIDE_OFF")


class SEQUENCER_PT_rig_settings(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_rig_settings"
    bl_label = "Rig Settings"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if not obj.tiny_rig.is_rig:
            self.layout.label(text="Rig not Found", icon="ARMATURE_DATA")
            return
        layout.label(text=f"Turnaround Length: {obj.tiny_rig.pose_length}")
        self.layout.operator("rigools.initialize_rig")
        layout.operator("rigools.set_pose_length")
        self.layout.operator("rigtools.apply_legacy_transforms")


classes = (
    SEQUENCER_PT_turnaround_editor,
    SEQUENCER_PT_rig_settings,
    SEQUENCER_PT_driver_editor,
    SEQUENCER_PT_rig_grease_pencil,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
