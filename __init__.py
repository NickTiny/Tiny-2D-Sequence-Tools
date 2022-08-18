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
import re
import bpy
from bpy import context
from operator import attrgetter
from bpy.utils import register_class, unregister_class


OldStrip = ""

prop_list = []


class VIEW3D_OP_constraint_to_strip_camera(bpy.types.Operator):
    bl_idname = "object.rotate_to_strip_camera"
    bl_label = "Enable Rotate to Strip Cameras to Active"

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({"ERROR"}, "There is no active object")
            return {"CANCELLED"}
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
        obj.rot_to_seq_cam = True
        context.scene.frame_set(int(context.scene.frame_current_final - 1))
        context.scene.frame_set(int(context.scene.frame_current_final + 1))
        return {"FINISHED"}


class VIEW3D_OP_constraint_to_strip_camera_remove(bpy.types.Operator):
    bl_idname = "object.remove_object_from_list"
    bl_label = "Disable Rotate to Strip Cameras from Active"

    def execute(self, context):
        rot_to_seq_cam = context.active_object.rot_to_seq_cam
        if rot_to_seq_cam is None:
            self.report({"ERROR"}, "Active Object is Not Rotated to Camera")
            return {"CANCELLED"}
        rot_to_seq_cam = False
        for obj in context.scene.objects:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    obj.constraints.remove(constraint)

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
    for obj in strip.scene.objects:
        if obj.rot_to_seq_cam:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    constraint.target = strip.scene_camera


class SEQUENCER_PT_constraint_to_strip_camera(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "SEQUENCER_PT_constraint_to_strip_camera"
    bl_label = "Constraint to Strip Cameras"
    bl_category = "Tiny Sequence Tools"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "object.rotate_to_strip_camera",
            text="Rotate Active Object to Strip Camera",
            icon="CON_ROTLIKE",
        )
        layout.operator("object.remove_object_from_list", icon="X")
        layout.separator()
        layout.label(text="Objects Rotated to Strip Cameras:", icon="OBJECT_DATA")

        for obj in context.active_sequence_strip.scene.objects:
            if obj.rot_to_seq_cam is True:
                box = layout.box()
                box.label(text=f"{obj.name}")
        # row.prop(
        #     context.window_manager.constraint_camera,
        #     "avaliable_properties",
        #     text="",
        # )


class VIEW3D_constraint_to_strip_object_panel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "constraint"
    bl_idname = "VIEW3D_sequencer_constraints"
    bl_label = "Rotate to Strip Camera"

    def draw(self, context):
        row = self.layout.row(align=True)
        row.label(text="Rotate to Strip Cameras")
        row.operator("object.rotate_to_strip_camera", icon="CON_ROTLIKE", text="Enable")
        if context.object.rot_to_seq_cam is True:
            row.operator("object.remove_object_from_list", icon="X", text="Disable")


def enum_items_generator(self, context):
    scene = context.active_sequence_strip.scene
    enum_items = []
    for obj in scene.objects:
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                enum_items.append(
                    (
                        str(constraint),
                        f"{constraint.id_data.name}",
                        f"{constraint.id_data.name} - {constraint.name}",
                    )
                )
    return enum_items


def get_rot_to_seq_cam_state(self):
    obj = self.id_data
    for constraint in obj.constraints:
        if constraint.type == "COPY_ROTATION":
            return True
    return False


def set_rot_to_seq_cam(self, value: bool):
    if not self:
        obj = self.id_data
        if obj.constraints is not None:
            for constraint in obj.constraints:
                if constraint.type == "COPY_ROTATION":
                    obj.constraints.remove(constraint)
        bpy.ops.object.constraint_add(type="COPY_ROTATION")
        for constraint in obj.constraints:
            if constraint.type == "COPY_ROTATION":
                prop_list.append(constraint)
                constraint.use_x = False
                constraint.use_y = False
                constraint.use_z = True
        return True


class constraint_to_camera_items(bpy.types.PropertyGroup):
    avaliable_properties: bpy.props.EnumProperty(
        items=enum_items_generator, name="Objects Rotated to Camera"
    )


@bpy.app.handlers.persistent
def constraint_to_camera_handler(self, context):
    update_constraint_camera(self)


classes = (
    SEQUENCER_PT_constraint_to_strip_camera,
    constraint_to_camera_items,
    VIEW3D_OP_constraint_to_strip_camera,
    VIEW3D_OP_constraint_to_strip_camera_remove,
    VIEW3D_constraint_to_strip_object_panel,
)


def register():
    bpy.app.handlers.frame_change_pre.append(constraint_to_camera_handler)
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.constraint_camera = bpy.props.PointerProperty(
        type=constraint_to_camera_items
    )
    bpy.types.Object.rot_to_seq_cam = bpy.props.BoolProperty(
        name="Enable Rotate to Strip Cameras",
        default=False,
        get=get_rot_to_seq_cam_state,
        set=set_rot_to_seq_cam,
        options=set(),
    )


def unregister():
    bpy.app.handlers.frame_change_pre.remove(constraint_to_camera_handler)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
