from tiny_seq_tools_master.line_art_tools.core import (
    check_animation_is_constant,
    make_animation_constant,
    check_keyframes_match_stnd,
    sync_seq_line_art,
    load_line_art_mods,
)
from tiny_seq_tools_master.line_art_tools.line_art_cam.core import (
    get_line_art_from_scene,  ## Exists because of LINEARTCAMBUG
)
import bpy


class lr_seq_items(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    mod_name: bpy.props.StringProperty()

    def get_thickness(self):
        obj = self.object
        if obj.type == "GPENCIL":
            return obj.grease_pencil_modifiers[self.mod_name].thickness
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

    status: bpy.props.BoolProperty(
        name="Keyframe Sync Status",
        get=get_status,
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


def get_line_art_seq_cam_state(self):
    obj = self
    if obj.grease_pencil_modifiers is None:
        return False
    for mod in obj.grease_pencil_modifiers:
        if mod.type == "GP_LINEART":
            if mod.use_custom_camera is True:
                return True
    return False


def set_line_art_seq_cam_state(self, value: bool):
    scenes = self.id_data.users_scene  ## Exists because of LINEARTCAMBUG
    if not self:
        obj = self
        for mod in obj.grease_pencil_modifiers:
            if mod.type == "GP_LINEART":
                if mod.use_custom_camera:
                    line_art_cam = get_line_art_from_scene(
                        scenes[0]
                    )  ## Exists because of LINEARTCAMBUG
                    mod.source_camera = line_art_cam  ## Exists because of LINEARTCAMBUG
                    return True
        return


classes = (lr_seq_items,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.line_art_list = bpy.props.CollectionProperty(type=lr_seq_items)
    bpy.types.Object.line_art_seq_cam = bpy.props.BoolProperty(
        name="Enable Seq Line Art Control",
        default=False,
        get=get_line_art_seq_cam_state,
        set=set_line_art_seq_cam_state,
        options=set(),
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
