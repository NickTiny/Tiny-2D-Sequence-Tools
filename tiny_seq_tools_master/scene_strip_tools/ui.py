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
        col.prop(
            manager,
            "link_seq_to_3d_view",
            text="Sync Strip Camera to 3D Viewport",
            icon="LINKED",
        )

        col.operator(
            "view3d.add_scene_strip",
            text="Add Camera as Scene Strip",
            icon="CAMERA_DATA",
        )
        col.prop(
            manager,
            "selection_to_active",
            text="Sync Strip Selection to Viewport",
        )

        col = layout.box()
        col.label(text="Render Strips")

        col.prop(
            context.scene.render,
            "filepath",
            text="Output",
        )

        col.operator("sequencer.preview_render", icon="FILE_MOVIE")
        set_row = col.row(align=True)
        set_row.operator("sequencer.batch_render", icon="RENDER_ANIMATION")
        set_row.operator("sequencer.setup_render", icon="SCENE_DATA", text="")


classes = (SEQUENCER_PT_scene_tools,)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)