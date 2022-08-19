from .core import sync_seq_line_art

import bpy


class SEQUENCER_OT_insert_keyframes(bpy.types.Operator):
    bl_idname = "view3d.key_line_art"
    bl_label = "Insert/Replace Line Art Keyframes"

    def execute(self, context):
        for item in context.active_sequence_strip.line_art_list:
            if item.status == False:
                obj = item.object
                for mod in obj.grease_pencil_modifiers:
                    if mod.type == "GP_LINEART":
                        sync_seq_line_art(context, mod)
        return {"FINISHED"}


classes = (SEQUENCER_OT_insert_keyframes,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
