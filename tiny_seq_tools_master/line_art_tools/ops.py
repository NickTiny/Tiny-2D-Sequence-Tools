from tiny_seq_tools_master.line_art_tools.core import (
    sync_seq_line_art,
)


import bpy


class SEQUENCER_OT_insert_keyframes(bpy.types.Operator):
    bl_idname = "view3d.key_line_art"
    bl_label = "Insert/Replace Line Art Keyframes"

    def execute(self, context):
        for item in context.scene.line_art_list:
            if item.status == False:
                obj = item.object
                for mod in obj.grease_pencil_modifiers:
                    if mod.type == "GP_LINEART":
                        sync_seq_line_art(context, mod)
        return {"FINISHED"}


class SEQUENCER_OT_add_line_art_obj(bpy.types.Operator):
    bl_idname = "view3d.add_line_art_obj"
    bl_label = "add_line_art_obj"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return (
            context.active_object
            and context.active_object.type == "GPENCIL"
            and not context.active_object.line_art_seq_cam
        )

    def execute(self, context):
        obj = context.active_object
        line_art_items = context.scene.line_art_list
        for index, item in enumerate(line_art_items):
            if item.object == obj:
                line_art_items.remove(index)

        for modifier in obj.grease_pencil_modifiers:
            if modifier.type == "GP_LINEART":
                modifier.use_custom_camera = True
                add_line_art_item = line_art_items.add()
                add_line_art_item.object = obj
                add_line_art_item.mod_name = modifier.name
        line_art_mod = obj.grease_pencil_modifiers["Line Art"]

        for strip in context.scene.sequence_editor.sequences_all:
            line_art_mod.keyframe_insert("thickness", frame=strip.frame_final_start)

        for fcurve in line_art_mod.id_data.original.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = "CONSTANT"

        obj.line_art_seq_cam = True

        return {"FINISHED"}


class SEQUENCER_OT_remove_line_art_obj(bpy.types.Operator):
    bl_idname = "view3d.remove_line_art_obj"
    bl_label = "remove_line_art_obj"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return (
            context.active_object
            and context.active_object.type == "GPENCIL"
            and context.active_object.line_art_seq_cam
        )

    def execute(self, context):
        obj = context.active_object
        # Remove from list of line_art_items
        for item in context.scene.line_art_list:
            line_art_items = context.scene.line_art_list
        for index, item in enumerate(context.scene.line_art_list):
            if item.object == obj:
                line_art_items.remove(index)

        # remove modifier
        # for modifier in obj.grease_pencil_modifiers:
        #     if modifier.type == "GP_LINEART":
        #         obj.grease_pencil_modifiers.remove(modifier)
        # add_line_art_item = context.scene.line_art_list.add()
        # add_line_art_item.object = obj

        # Set avaliablity to false
        obj.line_art_seq_cam = False

        return {"FINISHED"}


class SEQUENCER_OT_refresh_line_art_obj(bpy.types.Operator):
    bl_idname = "view3d.refresh_line_art_obj"
    bl_label = "refresh_line_art_obj"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return (
            context.active_sequence_strip
            and context.active_sequence_strip.type == "SCENE"
        )

    def execute(self, context):
        strip = context.active_sequence_strip
        line_art_items = context.scene.line_art_list
        line_art_items.clear()
        for obj in strip.scene.objects:
            if obj.line_art_seq_cam:
                add_line_art_item = line_art_items.add()
                add_line_art_item.object = obj
                add_line_art_item.mod_name = obj.grease_pencil_modifiers[0].name

        return {"FINISHED"}


classes = (
    SEQUENCER_OT_insert_keyframes,
    SEQUENCER_OT_add_line_art_obj,
    SEQUENCER_OT_remove_line_art_obj,
    SEQUENCER_OT_refresh_line_art_obj,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)