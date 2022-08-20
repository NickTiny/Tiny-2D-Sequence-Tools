from operator import iconcat
import bpy


class SEQUENCER_PT_line_art(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_line_art_tools"
    bl_label = "Active Line Art"
    bl_category = "Tiny Sequence Tools"

    def all_status_true(context):
        for item in context.scene.line_art_load.load:
            if item.status == False:
                return False
        return True

    def draw(self, context):

        self.layout.operator(
            "view3d.update_line_art_cam", icon="CAMERA_DATA"
        )  ## Exists because of LINEARTCAMBUG
        self.layout.separator()
        self.layout.prop(context.scene, "update_line_art_on_save")

        self.layout

        layout = self.layout
        col = layout.column()
        col = col.box()
        row = col.row(align=True)
        row.label(text="Sequence Line Art Items", icon="MOD_LINEART")
        row.operator("view3d.refresh_line_art_obj", icon="FILE_REFRESH", text="")
        if context.active_sequence_strip is None:
            return
        for item in context.scene.line_art_list:
            row = col.box()
            if item.status == False:
                row.alert = True
            row.prop(
                item, "thickness", slider=False, expand=False, text=item.object.name
            )


class VIEW3D_sequence_line_art_panel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "modifier"
    bl_idname = "VIEW3D_sequencer_line_art"
    bl_label = "Sequence Line Art"

    def draw(self, context):
        row = self.layout.row(align=True)
        row.label(text="Sequence Line Art")
        row.operator("view3d.add_line_art_obj", icon="MOD_LINEART", text="Enable")
        row.operator("view3d.remove_line_art_obj", icon="X", text="Disable")


classes = (SEQUENCER_PT_line_art, VIEW3D_sequence_line_art_panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
