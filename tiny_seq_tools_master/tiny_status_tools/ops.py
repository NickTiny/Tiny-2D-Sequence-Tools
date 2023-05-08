import bpy

def draw_status_checker(self, context):
    col = self.layout.column(align=False)
    col.separator()
    col.prop(context.scene.tiny_status, "file_path_status")
    col.prop(context.scene.tiny_status, "relative_links")
    col.prop(context.scene.tiny_status, "render_passes")
    col.prop(context.scene.tiny_status, "pack_status")



# Create operator to to transfer the current selection to the list.
class TINYSEQ_STATUS_OP_check_file_status(bpy.types.Operator):
    bl_label = "Check File Status"
    bl_description = "Check status of the following properties:\n Packed Images \n Render Output Path \n Relative Links \n Render Pass Settings"
    bl_idname = "tiny.check_file_status"
    bl_icon = "FILE_BLEND"

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        draw_status_checker(self, context)

    def execute(self, context):
        return {"FINISHED"}




def register():
    bpy.utils.register_class(TINYSEQ_STATUS_OP_check_file_status)


def unregister():
    bpy.utils.unregister_class(TINYSEQ_STATUS_OP_check_file_status)
