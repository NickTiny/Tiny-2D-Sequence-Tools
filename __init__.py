# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "constraint_to_strip_camera",
    "author": "Nick Alberelli ",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}

from os import remove
import bpy
from bpy import context
from operator import attrgetter
from bpy.utils import register_class, unregister_class


OldStrip = ""

prop_list = []


class constraint_to_strip_camera(bpy.types.Operator):
    bl_idname = "object.rotate_to_strip_camera"
    bl_label = "Rotate Object to Strip Camera"

    def execute(self, context):
        obj = context.active_object
        if obj.constraints is not None:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    obj.constraints.remove(constraint)
        window = context.window_manager.windows[0]
        with context.temp_override(window=window):
            bpy.ops.object.constraint_add(type="COPY_ROTATION")

        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                prop_list.append(constraint)
                constraint.use_x = False
                constraint.use_y = False
                constraint.use_z = True
        return {"FINISHED"}


def update_constraint_camera(scene):
    global OldStrip
    scn = scene
    seq = scn.sequence_editor.sequences
    seq = sorted(seq, key=attrgetter("channel", "frame_final_start"))
    cf = scn.frame_current
    for i in seq:
        try:
            if i.type == "SCENE" and i.name != OldStrip:
                if i.frame_final_start <= cf and i.frame_final_end > cf and not i.mute:
                    constraint_to_active_camera(i)
                    break
        except AttributeError:
            pass


def constraint_to_active_camera(strip):
    for prop in prop_list:
        prop.target = strip.scene_camera
    print("CONSTRAINT TO ACTIVE CAMERA")


class SEQUENCER_PT_constraint_to_strip_camera(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_constraint_to_strip_camera"
    bl_label = "Constraint to Strip Camera"
    bl_category = "Constraint to Camera"

    def draw(self, context):
        self.layout.prop(
            bpy.context.window_manager.constraint_camera,
            "avaliable_properties",
            text="",
        )
        self.layout.operator("object.rotate_to_strip_camera")


def enum_items_generator(self, context):
    enum_items = []
    if prop_list == []:
        return enum_items
    for e, d in enumerate(prop_list):
        enum_items.append((str(d), f"Obj: {d.id_data.name}", f"Mod:{d.name}"))
    return enum_items


class constraint_to_camera_items(bpy.types.PropertyGroup):
    avaliable_properties: bpy.props.EnumProperty(
        items=enum_items_generator, name="Select Target Property"
    )


@bpy.app.handlers.persistent
def constraint_to_camera_handler(self, context):
    update_constraint_camera(self)


classes = (
    SEQUENCER_PT_constraint_to_strip_camera,
    constraint_to_camera_items,
    constraint_to_strip_camera,
)


def register():
    bpy.app.handlers.frame_change_pre.append(constraint_to_camera_handler)
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.constraint_camera = bpy.props.PointerProperty(
        type=constraint_to_camera_items
    )


def unregister():
    bpy.app.handlers.frame_change_pre.remove(constraint_to_camera_handler)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
