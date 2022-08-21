import bpy


class TINYSEQ_STATUS_PG_sequencer(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "3DVIEW_PT_tiny_status_sequencer"
    bl_label = "Tiny Status"
    bl_category = "Tiny Sequence Tools"

    def draw(self, context):
        self.layout.operator("relay.get_selection_tiny", icon="FILE_BLEND")


classes = [
    TINYSEQ_STATUS_PG_sequencer,
]


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
