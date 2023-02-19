import bpy


class SEQUENCER_PT_scene_tools(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_scene_tools"
    bl_label = "Scene Strip Tools"
    bl_category = "Tiny Sequence Tools"

    def draw(self, context):
        layout = self.layout
        col = layout.box()
        row = col.row(align=False)
        row.label(text="Render Strips")

        col.prop(
            context.scene.render,
            "filepath",
            text="Output",
        )
        col.prop(context.window_manager.render_settings, "render_preview_range")
        if context.window_manager.render_settings.render_preview_range:
            row = col.row(align=True)
            row.prop(context.window_manager.render_settings, "render_start")
            row.prop(context.window_manager.render_settings, "render_end")
        col.operator("sequencer.preview_render", icon="FILE_MOVIE")
        set_row = col.row(align=True)
        set_row.operator("sequencer.tiny_full_render", icon="RENDER_ANIMATION")
        set_row.operator("sequencer.setup_render", icon="SCENE_DATA", text="")


class SEQUENCER_PT_camera_from_view(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_camera_from_view"
    bl_label = "Camera from View"
    bl_category = "Add Camera"

    def draw(self, context):
        self.layout.operator(
            "sequencer.add_camera_from_view",
        )


classes = (SEQUENCER_PT_scene_tools, SEQUENCER_PT_camera_from_view)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
