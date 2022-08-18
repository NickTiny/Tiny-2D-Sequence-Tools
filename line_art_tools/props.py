from .core import (
    check_animation_is_constant,
    make_animation_constant,
    check_keyframes_match_stnd,
    sync_seq_line_art,
    load_line_art_mods,
)
import bpy


class lr_seq_items(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    mod_name: bpy.props.StringProperty()

    def get_thickness(self):
        obj = self.object
        if obj.type == "GPENCIL":
            for mod in obj.grease_pencil_modifiers:
                if mod.type == "GP_LINEART":
                    return mod.thickness
            return mod.thickness
        return 0

    def set_thickness(self, thickness: int):

        frame = self.id_data.sequence_editor.active_strip.frame_final_start
        if frame > self.id_data.sequence_editor.active_strip.scene.frame_current_final:
            return
        if self.id_data.objects is None:
            return 0
        obj = self.object
        line_art_mod = [
            mod for mod in obj.grease_pencil_modifiers if mod.type == "GP_LINEART"
        ]
        fcurves = obj.animation_data.action.fcurves
        keyframes = fcurves[0].keyframe_points
        for mod in line_art_mod:
            mod.thickness = thickness
            mod.keyframe_insert("thickness", frame=frame)
            if check_animation_is_constant(mod) == False:
                make_animation_constant(mod)

        for key in keyframes:
            if key.co[0] in range(
                frame, self.id_data.sequence_editor.active_strip.frame_final_end
            ):
                if key.co[0] == frame:
                    key.co[1] = thickness
                if key.co[0] in range(
                    frame + 1, self.id_data.sequence_editor.active_strip.frame_final_end
                ):
                    for mod in line_art_mod:
                        mod.keyframe_delete("thickness", frame=key.co[0])

        return

    def get_status(self):
        return check_keyframes_match_stnd(self)

    def set_status(self, status: bool):
        obj = self.object
        line_art_mod = [
            mod for mod in obj.grease_pencil_modifiers if mod.type == "GP_LINEART"
        ]
        fcurves = obj.animation_data.action.fcurves
        keyframes = fcurves[0].keyframe_points
        if fcurves is None:
            return
        frame = self.id_data.sequence_editor.active_strip.frame_final_start
        for key in keyframes:
            if key[0] in range(
                frame + 1, self.id_data.sequence_editor.active_strip.frame_final_end
            ):
                for mod in line_art_mod:
                    mod.keyframe_delete("thickness", frame=key.co[0])

        for mod in obj.grease_pencil_modifiers:
            if mod.type == "GP_LINEART":
                sync_seq_line_art(self.id_data.sequence_editor.active_strip.scene, mod)
        status = True
        return status

    status: bpy.props.BoolProperty(
        name="Keyframe Sync Status",
        get=get_status,
        set=set_status,
        options=set(),
        description="Line Art keyframes are out of sync with the sequencer, please update by adjusting the thickness to update keyframes or adjust manually.",
    )
    thickness: bpy.props.IntProperty(
        name="Line Art Seq",
        default=0,
        get=get_thickness,
        set=set_thickness,
        options=set(),
    )


def check_list_status(list):
    if len(list) != 0:
        return True
    else:
        return False


class lr_seq_load(bpy.types.PropertyGroup):
    def get_line(self):
        strip = self.id_data.original.sequence_editor.active_strip
        if strip.line_art_list != None:
            return check_list_status(strip.line_art_list)

    def set_line(self, status: bool):
        strip = self.id_data.original.sequence_editor.active_strip
        load_line_art_mods(strip)
        return status

    def get_error(self):
        for strip in self.id_data.sequence_editor.sequences_all:
            for item in strip.line_art_list:
                if item.status == False:
                    return False
        return True

    load: bpy.props.BoolProperty(
        name="Load Line Art Objects",
        get=get_line,
        set=set_line,
        options=set(),
        description="",
    )

    error: bpy.props.BoolProperty(
        name="Line ARt Error",
        get=get_error,
    )


classes = (
    lr_seq_items,
    lr_seq_load,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.line_art_load = bpy.props.PointerProperty(type=lr_seq_load)
    bpy.types.Sequence.line_art_list = bpy.props.CollectionProperty(type=lr_seq_items)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
