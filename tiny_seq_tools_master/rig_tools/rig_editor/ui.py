import bpy

from tiny_seq_tools_master.core_functions.drivers import get_driver_ob_obj


class SEQUENCER_PT_turnaround_editor(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_turnaround_editor"
    bl_label = "Turnaround Editor"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        self.layout(context.window_manager, "offset_editor_active")
        obj = context.active_object
        layout = self.layout
        action_row = layout.row(align=True)
        # if not obj.tiny_rig.is_rig:
        #     self.layout.label(text="Rig not Found", icon="ARMATURE_DATA")
        #     return

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
        layout.operator("rigools.create_2d_armature")
        
        
class SEQUENCER_PT_rig_grease_pencil(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_rig_grease_pencil"
    bl_label = "Rig Grease Pencil"
    bl_category = "Tiny Rig Edit"

    def draw(self, context):
        layout = self.layout
        layout.operator("rigools.gp_constraint_armature")


class SEQUENCER_PT_edit_grease_pencil(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_edit_grease_pencil"
    bl_label = "Rigged Grease Pencil Draw Helper"
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

    bpy.types.Scene.obj_selection = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.bone_selection = bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        self.layout.prop_search(
                context.scene, "bone_selection", obj.id_data.pose, "bones", text="Property Bone"
            )
        self.layout.operator("rigools.initialize_rig")
        if not obj.tiny_rig.is_rig:
            self.layout.label(text="Rig not Found", icon="ARMATURE_DATA")
            return
        layout.label(text=f"Turnaround Length: {obj.tiny_rig.pose_length}")        
class SEQUENCER_PT_rig_properties(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_rig_properties"
    bl_label = "Rig Properties"
    bl_category = "Tiny Rig Edit"
    bl_parent_id = "SEQUENCER_PT_rig_settings"

    def draw(self, context):
               
        obj = context.active_object
        prop_col = self.layout.box()
        
        try:
            prop_bone = obj.pose.bones[context.scene.bone_selection]
            if len(prop_bone.keys()) == 0:
                prop_col.label(text = f"No Properties on '{prop_bone.name}'")
            for x in prop_bone.keys():
                prop_col.prop(prop_bone, f'["{x}"]') 
        except KeyError:
            prop_col.label(text = "No Property Bone Found")
            return
        

        



classes = (
    SEQUENCER_PT_turnaround_editor,
    SEQUENCER_PT_rig_settings,
    SEQUENCER_PT_rig_properties,
    SEQUENCER_PT_edit_grease_pencil,
    SEQUENCER_PT_rig_grease_pencil,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
