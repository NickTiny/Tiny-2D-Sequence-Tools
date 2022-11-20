from tiny_seq_tools_master.line_art_tools.core import (
    sync_line_art_obj_to_strip,
    set_seq_line_art_thickness,
)
import bpy


def check_gp_obj_modifiers(obj):
    if obj.grease_pencil_modifiers:
        return True
    return False


class lr_seq_items(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(type=bpy.types.Object)

    def get_thickness(self):
        obj = self.object
        if check_gp_obj_modifiers(obj):
            if obj.type == "GPENCIL" and len(obj.users_scene) != 0:
                return int(obj.grease_pencil_modifiers["SEQ_LINE_ART"].thickness)
        return 0

    def set_thickness(self, thickness: int):
        scene = bpy.context.scene
        if scene.sequence_editor and scene.sequence_editor.active_strip:
            strip = scene.sequence_editor.active_strip
            set_thick_done = set_seq_line_art_thickness(self.object, thickness, strip)
            if set_thick_done:
                return

    def get_status(self):
        scene = bpy.context.scene
        obj = self.object
        if check_gp_obj_modifiers(obj):
            if scene.sequence_editor and scene.sequence_editor.active_strip:
                strip = scene.sequence_editor.active_strip
                if strip:
                    return sync_line_art_obj_to_strip(self.object, strip)
        else:
            return 0

    def get_viewport(self):
        obj = self.object
        if check_gp_obj_modifiers(obj):
            if self.object.grease_pencil_modifiers["SEQ_LINE_ART"]:
                return self.object.grease_pencil_modifiers["SEQ_LINE_ART"].show_viewport
        return

    def set_viewport(self, val: bool):
        self.object.grease_pencil_modifiers["SEQ_LINE_ART"].show_viewport = val

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
    viewport: bpy.props.BoolProperty(
        name="Viewport Display Seq Line Art",
        get=get_viewport,
        set=set_viewport,
        options=set(),
        description="Hide and Show Line Art Modifiers in Viewports",
    )


classes = (lr_seq_items,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.line_art_seq_items = bpy.props.CollectionProperty(
        type=lr_seq_items
    )
    bpy.types.WindowManager.line_art_cam_override = bpy.props.BoolProperty(
        name="Override Camera",
        description="Render Line Art from the Tiny Line Art camera (which needs to be refreshed)",
        default=False,
    )
    bpy.types.Object.line_art_seq_obj = bpy.props.BoolProperty(
        name="Enable Seq Line Art Control",
        description="Control Line Art Object from Sequence",
        default=False,
    )
    bpy.types.WindowManager.use_seq_line_art = bpy.props.BoolProperty(
        name="Enable Seq Line Art",
        description="Control Line Art Object from Sequence",
        default=False,
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.use_seq_line_art
    del bpy.types.Object.line_art_seq_obj
    del bpy.types.WindowManager.line_art_cam_override
    del bpy.types.WindowManager.line_art_seq_items
