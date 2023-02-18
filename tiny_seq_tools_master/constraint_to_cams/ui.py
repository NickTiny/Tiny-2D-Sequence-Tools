import bpy

class SEQUENCER_PT_constraint_to_strip_camera(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_constraint_to_strip_camera"
    bl_label = "Rotate to Camera"
    bl_category = "Tiny Sequence Tools"

    def draw(self, context):
        layout = self.layout
        col = layout.box()
        row = col.row()
        row.label(text="Rotate to Strip Cameras:", icon="OBJECT_DATA")
        row.operator("object.refresh_copy_rot_items", icon="FILE_REFRESH", text="")
        rot_to_seq_cam_items = context.window_manager.rot_to_seq_cam_items

        if len(rot_to_seq_cam_items) == 0:
            col.alert = True
            col.label(text="NO ITEMS", icon="ERROR")

        for item in rot_to_seq_cam_items:
            obj = item.object
            box = col.box()
            box.label(text=f"{obj.name}")


class VIEW3D_constraint_to_strip_object_panel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "constraint"
    bl_idname = "VIEW3D_PT_sequencer_constraints"
    bl_label = "Rotate to Strip Camera"

    def draw(self, context):
        row = self.layout.row(align=True)
        row.label(text="Rotate to Strip Cameras")
        row.operator("object.rotate_to_strip_camera", icon="CON_ROTLIKE", text="Enable")
        row.operator("object.remove_object_from_list", icon="X", text="Disable")


classes = (
    SEQUENCER_PT_constraint_to_strip_camera,
    VIEW3D_constraint_to_strip_object_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
