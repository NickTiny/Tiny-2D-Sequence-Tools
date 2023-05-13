import bpy


class SEQUENCER_PT_scene_tools(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_scene_tools"
    bl_label = "Scene Strip Tools"
    bl_category = "Tiny Sequence Tools"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=(False))
        col = col.box()
        manager = context.scene
        row = col.row(align=True)
        row.label(text="Sequencer Sync", icon="UV_SYNC_SELECT")
        row.operator(
            "sequencer.fix_viewport_sync_errors",
            icon="ERROR",
        )
        row = col.row(align=True)
        row.prop(manager, "link_seq_to_3d_view", text="")
        row.separator()
        row.label(
            text="Sync Strip Camera to 3D Viewport",
            icon="LINKED",
        )
        row = col.row(align=True)
        row.prop(manager, "selection_to_active", text="")
        row.separator()
        row.label(text="Sync Strip Selection to Viewport", icon="SEQ_STRIP_META")
        col.operator(
            "view3d.add_scene_strip",
            text="Add Camera as Scene Strip",
            icon="CAMERA_DATA",
        )

        strip = context.scene.sequence_editor.active_strip
        col = layout.box()
        row = col.row(align=True)
        row.label(text="", icon="SEQUENCE")
        if strip:
            row.template_ID(strip, "scene_camera", text=f"{strip.name}")
        else:
            row.label(text="No Scene Strip Active!")
        row.operator("sequencer.refresh_viewport_camera", icon="FILE_REFRESH", text="")

        col = layout.box()
        row = col.row(align=False)
        row.label(text="Render Strips")

        col.prop(
            context.scene.render,
            "filepath",
            text="Output",
        )
        set_row = col.row(align=True)
        layout = col
        layout.use_property_split = True
        options = context.scene.batch_render_options
        layout.prop(options, "render_engine")
        layout.prop(options, "resolution")
        if options.media_type == "MOVIE":
            layout.prop(options, "frames_handles")
        layout.prop(options, "selection_only")
        box = layout.box()
        box.prop(options, "output_scene")
        layout.operator("sequencer.batch_render")


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
