import bpy


class SEQUENCER_PT_line_art(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_line_art_tools"
    bl_label = "Active Strip Line Art"
    bl_category = "Tiny Sequence Tools"

    def all_status_true(context):
        for item in context.scene.line_art_load.load:
            if item.status == False:
                return False
        return True

    def draw(self, context):

        layout = self.layout
        col = layout.column(align=False)
        row = col.row(align=True)
        row.prop(context.scene, "line_art_cam_override", text="")
        row.label(text="Override Line Art Camera", icon="CAMERA_DATA")
        if context.scene.line_art_cam_override:
            row = col.row(align=True)
            row.prop(
                context.scene,
                "update_line_art_on_save",
                text="",
            )
            row.label(text="Refresh Override Camera on Save", icon="FILE_TICK")
            if context.scene.update_line_art_on_save:
                row = col.row(align=True)
                row.alert = True
                row.separator(factor=4)
                row.label(
                    text="Refresh Override Camera on Save can be slow", icon="ERROR"
                )
                row = col.row(align=True)

            col.operator("view3d.update_line_art_cam", icon="FILE_REFRESH")

        col = layout.box()
        row = col.row(align=False)
        row.label(text="Sequence Line Art Items", icon="MOD_LINEART")
        row.operator("view3d.check_line_art_obj", icon="ERROR", text="Check Line Art")
        row.operator("view3d.update_similar_strip_line_art", icon="DUPLICATE", text="")
        row.operator("view3d.refresh_line_art_obj", icon="FILE_REFRESH", text="")

        if context.active_sequence_strip is None:
            return
        for item in context.scene.line_art_list:
            box = col.box()
            row = box.row(align=True)
            if item.status == False:
                row.alert = True
            row.prop(
                item, "thickness", slider=False, expand=False, text=item.object.name
            )
            row.prop(
                item,
                "viewport",
                slider=False,
                expand=False,
                text="",
                icon="RESTRICT_VIEW_OFF",
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
