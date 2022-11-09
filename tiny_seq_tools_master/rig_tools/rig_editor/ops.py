import bpy


pbone_name = "PoseData"

from tiny_seq_tools_master.core_functions.bone import (
    apply_transforms_on_frame,
    get_consts_on_bone,
    reset_bones,
    show_hide_constraints,
)

from tiny_seq_tools_master.rig_tools.rig_editor.core import (
    get_action_offset_bones,
    get_action_from_constraints,
)

from tiny_seq_tools_master.core_functions.drivers import add_driver


class RIGTOOLS_toggle_enable_action(bpy.types.Operator):
    bl_idname = "rigools.enable_offset_action"
    bl_label = "Edit Offset Action"
    bl_description = "Offset Action Editor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object.animation_data.action
            != context.active_object.offset_action
        )

    def execute(self, context):
        obj = context.active_object
        offset_action = obj.offset_action
        if not offset_action:
            self.report({"ERROR"}, "Offset Action not Set")
            return {"CANCELLED"}
        if obj.animation_data.action == offset_action:
            self.report({"ERROR"}, "Offset Action already Enabled")
            return {"CANCELLED"}
        obj.animation_data.action = None
        reset_bones(obj.pose.bones)
        constraints = get_action_offset_bones(obj.pose.bones)
        show_hide_constraints(constraints, False)
        obj.animation_data.action = offset_action
        self.report({"INFO"}, "Offset Editing Enabled!")
        return {"FINISHED"}


class RIGTOOLS_toggle_disable_action(bpy.types.Operator):
    bl_idname = "rigools.disable_offset_action"
    bl_label = "Disable Offset Action Editing"
    bl_description = "Offset Action Editor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object.animation_data.action
            == context.active_object.offset_action
        )

    def execute(self, context):
        obj = context.active_object
        offset_action = obj.offset_action
        if not offset_action:
            self.report({"ERROR"}, "Offset Action not Set")
            return {"CANCELLED"}
        if not obj.animation_data.action == offset_action:
            self.report({"ERROR"}, "Offset Action not Enabled")
            return {"CANCELLED"}
        obj.animation_data.action = None
        reset_bones(obj.pose.bones)
        constraints = get_action_offset_bones(obj.pose.bones)
        show_hide_constraints(constraints, True)
        self.report({"INFO"}, "Offset Editing Disabled!")
        return {"FINISHED"}


class RIGTOOLS_load_action(bpy.types.Operator):
    bl_idname = "rigools.load_action"
    bl_label = "Load Offset Action"
    bl_description = "Offset Action"
    bl_options = {"UNDO"}

    def execute(self, context):
        offset_action = get_action_from_constraints(context.active_object.pose.bones)
        context.active_object.offset_action = offset_action
        return {"FINISHED"}


class RIGTOOLS_add_action_const_to_bone(bpy.types.Operator):
    bl_idname = "rigools.add_action_const_to_bone"
    bl_label = "Add Body Offset Driver to Selected"
    bl_description = """If a bone is included in the active_object's 'Offset Action' add constraint to move bone via action constraint. 
    This will also add a driver back to the Body/Head Poses"""
    bl_options = {"UNDO"}

    def execute(self, context):
        action_length = int(context.active_object.offset_action.frame_range[1])
        for bone in context.selected_pose_bones:
            if not get_consts_on_bone(bone, "ACTION"):
                new = bone.constraints.new("ACTION")
                new.action = bone.id_data.offset_action
                new.use_eval_time = True
                add_driver(
                    bone.id_data,
                    bone.id_data,
                    "Pose",
                    f'pose.bones["{bone.name}"].constraints["{new.name}"].eval_time',
                    'pose.bones["PoseData"]["Pose"]',
                    -1,
                    f"Pose/{action_length}",
                )
                new.frame_end = action_length
        return {"FINISHED"}


class RIGTOOLS_add_action_const_to_bone_head(bpy.types.Operator):
    bl_idname = "rigools.add_action_const_to_bone_head"
    bl_label = "Add Head Offset Driver to Selected"
    bl_description = """If a bone is included in the active_object's 'Offset Action' add constraint to move bone via action constraint. 
    This will also add a driver back to the Body/Head Poses"""
    bl_options = {"UNDO"}

    def execute(self, context):
        action_length = int(context.active_object.offset_action.frame_range[1])
        for bone in context.selected_pose_bones:
            if not get_consts_on_bone(bone, "ACTION"):
                new = bone.constraints.new("ACTION")
                new.action = bone.id_data.offset_action
                new.use_eval_time = True
                add_driver(
                    bone.id_data,
                    bone.id_data,
                    "Pose_Head",
                    f'pose.bones["{bone.name}"].constraints["{new.name}"].eval_time',
                    'pose.bones["PoseData"]["Pose Head"]',
                    -1,
                    f"Pose_Head/{action_length}",
                )
                new.frame_end = action_length
        return {"FINISHED"}


class RIGTOOLS_apply_legacy_transforms(bpy.types.Operator):
    bl_idname = "rigtools.apply_legacy_transforms"
    bl_label = "Apply Legacy Constraints on Current Frame"
    bl_description = (
        """Apply Legacy Transform Constraints on Current Frame for selected bones"""
    )
    bl_options = {"UNDO"}

    def execute(self, context):
        apply_transforms_on_frame(
            context.scene.frame_current, context.selected_pose_bones
        )
        return {"FINISHED"}


class RIGTOOLS_add_ik_fk_toggle(bpy.types.Operator):
    bl_idname = "rigtools.add_ik_fk_toggle"
    bl_label = "Add IK Toggle"
    bl_description = """Add Prop to Posebone, drive influence of IK constraint and Copy Rotation of hand."""
    bl_options = {"UNDO"}

    def execute(self, context):
        # From selected IK Bone
        bone = context.active_pose_bone
        base_name = bone.name.split(".")[0]
        print(base_name)

        # Add Prop to Bone
        propbone = context.active_object.pose.bones[pbone_name]
        if bone is propbone:
            self.report({"ERROR"}, f"Active Bone Cannot Be {propbone.name}")
            return {"CANCELLED"}

        # get IK Influence Path
        constraint = None
        for const in bone.constraints:
            if const.type == "IK":
                constraint = const

        if constraint is None:
            self.report({"ERROR"}, f"Active Bone must have IK")
            return {"CANCELLED"}

        ik_prop_name = f"{base_name}_IK"
        propbone[ik_prop_name] = 1

        # get or create the UI object for the property
        ui = propbone.id_properties_ui(ik_prop_name)
        ui.update(default=1)
        ui.update(min=0)
        ui.update(max=1)

        datapath = propbone[ik_prop_name]

        add_driver(
            bone.id_data,
            bone.id_data,
            ik_prop_name,
            f'pose.bones["{bone.name}"].constraints["{constraint.name}"].influence',
            f'pose.bones["{propbone.name}"]["{ik_prop_name}"]',
            -1,
        )

        return {"FINISHED"}


classes = (
    RIGTOOLS_add_ik_fk_toggle,
    RIGTOOLS_apply_legacy_transforms,
    RIGTOOLS_add_action_const_to_bone_head,
    RIGTOOLS_add_action_const_to_bone,
    RIGTOOLS_toggle_enable_action,
    RIGTOOLS_toggle_disable_action,
    RIGTOOLS_load_action,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
