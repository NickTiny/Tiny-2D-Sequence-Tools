import bpy


class TINYSEQ_STATUS_PG(bpy.types.PropertyGroup):
    def check_render_path(self):
        scene = bpy.context.scene
        if scene is None:
            return
        if not scene.render.filepath.startswith("//"):
            return False
        return True

    def set_render_path(self, context):

        scene = bpy.context.scene
        name = bpy.path.basename(bpy.context.blend_data.filepath.replace(".blend", ""))
        scene.render.filepath = f"//Render/{name}"

    file_path_status: bpy.props.BoolProperty(
        name="Render Output Path",
        get=check_render_path,
        set=set_render_path,
        options=set(),
        description="Ensure render output is set to relative path.",
    )

    def check_linked_files(self):
        if len(bpy.data.libraries) == 0:
            return True
        for lib in bpy.data.libraries:
            if not lib.filepath.startswith("//"):
                return False
            return True

    def set_linked_files(self, context):
        bpy.ops.file.make_paths_relative()
        for lib in bpy.data.libraries:
            if not lib.filepath.startswith("//"):
                return
        return None

    relative_links: bpy.props.BoolProperty(
        name="Linked Files",
        get=check_linked_files,
        set=set_linked_files,
        options=set(),
        description="Ensure linked files are set to relative paths and all linked files.",
    )

    def check_render_settings(self):
        scene = bpy.context.scene
        for layer in scene.view_layers:
            if layer.use_pass_combined == False:
                return False
            if layer.use_pass_z == False:
                return False
        return True

    def set_render_settings(self, context):
        scene = bpy.context.scene
        for layer in scene.view_layers:
            layer.use_pass_combined = True
            layer.use_pass_z = True
        return None

    render_passes: bpy.props.BoolProperty(
        name="Render Pass Settings",
        get=check_render_settings,
        set=set_render_settings,
        options=set(),
        description="Ensure under VIEW LAYER, both 'Combine' and 'Z' passes are enabled.",
    )

    def check_pack_status(self):
        return bpy.data.use_autopack

    def set_pack_status(self, context):
        if not bpy.data.use_autopack:
            bpy.ops.file.autopack_toggle()
        return 

    pack_status: bpy.props.BoolProperty(
        name="Images Packed",
        get=check_pack_status,
        set=set_pack_status,
        options=set(),
        description="Ensure images are packed.",
    )


classes = [
    TINYSEQ_STATUS_PG,
]


def register():
    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.Scene.tiny_status = bpy.props.PointerProperty(type=TINYSEQ_STATUS_PG)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
