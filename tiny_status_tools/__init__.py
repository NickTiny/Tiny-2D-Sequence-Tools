import bpy
from bpy.utils import register_class, unregister_class


# class TINYSTATUS_OT_status_checker(bpy.types.Operator):
#     bl_idname = "3DVIEW_PT_tiny_check"
#     bl_label = "Tiny Status"

#     def execute(self, context):
#         for status in context.scene.tiny_status:
#             if status == True:
#                 print(status.name)
#         return {"FINISHED"}


class TINYSTATUS_PT(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "3DVIEW_PT_tiny_status"
    bl_label = "Tiny Status"
    bl_category = "File Status"

    def draw(self, context):
        self.layout.prop(context.scene.tiny_status, "file_path_status")
        self.layout.prop(context.scene.tiny_status, "relative_links")
        self.layout.prop(context.scene.tiny_status, "render_passes")
        self.layout.prop(context.scene.tiny_status, "external_images")


class TINYSTATUS_PG(bpy.types.PropertyGroup):
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
        description="Ensure linked files are set to relative paths and all linked files are within BLOWN APART folder.",
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

    def get_external_images(self):
        if len(bpy.data.images) != 1:
            for image in bpy.data.images:
                if len(image.packed_files) == 0:
                    return False
        return True

    def set_external_images(self, context):
        bpy.ops.file.pack_all()
        if len(bpy.data.images) == 1:
            return
        for image in bpy.data.images:
            if len(image.packed_files) == 0:
                return
        return None

    external_images: bpy.props.BoolProperty(
        name="Images Packed",
        description="Ensure images are packed into this .blend",
        default=True,
        get=get_external_images,
        set=set_external_images,
        options=set(),
    )


classes = [
    TINYSTATUS_PG,
    TINYSTATUS_PT,
]
# TINYSTATUS_OT_status_checker


def register():
    for i in classes:
        register_class(i)
    bpy.types.Scene.tiny_status = bpy.props.PointerProperty(type=TINYSTATUS_PG)


def unregister():
    for i in classes:
        unregister_class(i)
