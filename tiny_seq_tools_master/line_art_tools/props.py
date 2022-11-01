from tiny_seq_tools_master.line_art_tools.core import (
    sync_line_art_obj_to_strip,
    set_seq_line_art_thickness,
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
        strip = self.id_data.sequence_editor.active_strip
        set_thick_done = set_seq_line_art_thickness(self.object, thickness, strip)
        if set_thick_done:
            return

    def get_status(self):
        scene = self.id_data
        strip = scene.sequence_editor.active_strip
        if strip:
            return sync_line_art_obj_to_strip(self.object, strip)

    def get_viewport(self):
        for modifier in self.object.grease_pencil_modifiers:
            if modifier.type == "GP_LINEART":
                return modifier.show_viewport

    def set_viewport(self, val: bool):
        for modifier in self.object.grease_pencil_modifiers:
            if modifier.type == "GP_LINEART":
                modifier.show_viewport = val

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
    bpy.types.Scene.line_art_seq_items = bpy.props.CollectionProperty(type=lr_seq_items)
    bpy.types.Scene.line_art_cam_override = bpy.props.BoolProperty(
        name="Override Camera",
        description="Render Line Art from the Tiny Line Art camera (which needs to be refreshed)",
        default=False,
    )
    bpy.types.Object.line_art_seq_obj = bpy.props.BoolProperty(
        name="Enable Seq Line Art Control",
        description="Control Line Art Object from Sequence",
        default=False,
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
