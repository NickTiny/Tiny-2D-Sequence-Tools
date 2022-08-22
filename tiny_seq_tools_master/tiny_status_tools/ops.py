import bpy


class TINYSEQ_STATUS_OP_pack_all_images(bpy.types.Operator):
    bl_label = "Check all images are packed"
    bl_description = "Ensure all Images are packed into this .blend"
    bl_idname = "tiny.check_all_images_are_packed"

    def execute(self, context):
        if len(bpy.data.images) == 1:
            self.report({"INFO"}, "All Avaliable Images packed")
            return {"FINISHED"}
        bpy.ops.file.pack_all()
        for image in bpy.data.images:
            if len(image.packed_files) == 0:
                self.report({"INFO"}, "Images failed to pack")
                return {"CANCELLED"}
        self.report({"INFO"}, "All Avaliable Images packed")
        return {"FINISHED"}


# Create operator to to transfer the current selection to the list.
class TINYSEQ_STATUS_OP_check_file_status(bpy.types.Operator):
    bl_label = "Check File Status"
    bl_description = "Check status of the following properties:\n Packed Images \n Render Output Path \n Relative Links \n Render Pass Settings"
    bl_idname = "relay.get_selection_tiny"
    bl_icon = "FILE_BLEND"

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column(align=False)
        col.operator("tiny.check_all_images_are_packed", icon="FILE_IMAGE")
        col.operator("sequencer.check_viewport_sync_errors")
        col.separator()
        col.prop(context.scene.tiny_status, "file_path_status")
        col.prop(context.scene.tiny_status, "relative_links")
        col.prop(context.scene.tiny_status, "render_passes")

    def execute(self, context):
        return {"FINISHED"}


classes = (TINYSEQ_STATUS_OP_pack_all_images, TINYSEQ_STATUS_OP_check_file_status)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
