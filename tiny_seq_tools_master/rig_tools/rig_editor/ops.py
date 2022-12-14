import bpy


pbone_name = "PoseData"

from tiny_seq_tools_master.core_functions.bone import (
    apply_transforms_on_frame,
    get_consts_on_bone,
    reset_bones,
    show_hide_constraints,
    add_action_const_to_head,
    add_action_const_to_body,
)

from tiny_seq_tools_master.rig_tools.rig_editor.core import (
    get_action_offset_bones,
    get_action_from_constraints,
    hide_grease_pencil_editor,
    enable_all_mod_const,
)

from tiny_seq_tools_master.core_functions.drivers import add_driver, get_driver_ob_obj

from tiny_seq_tools_master.core_functions.object import (
    check_object_type,
    get_consts_on_obj,
)


class RIGTOOLS_rig_edit_base_class(bpy.types.Operator):
    """Base Class for all Rig Edit Operations"""

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        res = not (obj.library or obj.override_library)
        if not res:
            cls.poll_message_set("Cannot Edit Reference Objects")
        return res


class RIGTOOLS_enter_grease_pencil_editor(bpy.types.Operator):
    bl_idname = "rigools.enter_grease_pencil_editor"
    bl_label = "Edit Selected Grease Pencil"
    bl_description = "Edit Selected Grease Pencil"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        res = not (
            obj.library
            or obj.override_library
            or context.window_manager.gpencil_editor_active
        )
        if not res:
            cls.poll_message_set("Cannot Edit Reference Objects")
        return res

    def execute(self, context):
        obj = context.active_object
        obj_type = "GPENCIL"
        if not check_object_type(obj, obj_type):
            self.report({"ERROR"}, f"Active Object type must be {obj_type}")
            return {"CANCELLED"}
        if hide_grease_pencil_editor(obj, False) is False:
            self.report({"ERROR"}, f"{obj.name} failed to enter draw mode")
            return {"CANCELLED"}
        context.window_manager.gpencil_editor_active = obj.data
        self.report({"INFO"}, f"{obj.name} entered draw mode")
        return {"FINISHED"}


class RIGTOOLS_enter_grease_pencil_editor_exit(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.enter_grease_pencil_editor_exit"
    bl_label = "Exit Edit Selected Grease Pencil"
    bl_description = "Exit Edit on Selected Grease Pencil"
    bl_options = {"UNDO"}

    def execute(self, context):
        obj = context.active_object
        obj_type = "GPENCIL"
        if not check_object_type(obj, obj_type):
            self.report({"ERROR"}, f"Active Object type must be {obj_type}")
            return {"CANCELLED"}
        if hide_grease_pencil_editor(obj, True) is False:
            self.report({"ERROR"}, f"{obj.name} failed to enter draw mode")
            return {"CANCELLED"}
        context.window_manager.gpencil_editor_active = None
        self.report({"INFO"}, f"{obj.name} exited draw mode")
        return {"FINISHED"}


class RIGTOOLS_isolate_gpencil(bpy.types.Operator):
    bl_idname = "rigools.isolate_gpencil"
    bl_label = "Isolate Selected Grease Pencil"
    bl_description = "Toggles Isolation for objects in the current scene"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.view3d.localview(frame_selected=True)
        return {"FINISHED"}


class RIGTOOLS_enable_all_gp_mod_const(bpy.types.Operator):
    bl_idname = "rigools.enable_all_gp_mod_const"
    bl_label = "Check all Grease Pencil Objects"
    bl_description = "Ensure all Grease Pencil Modifiers are enabled if any are not."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        enable_all_mod_const(context.active_object, True)
        self.report({"INFO"}, "All Modifiers and Constraints are Enabled!")
        return {"FINISHED"}


old_action = None


class RIGTOOLS_initialize_rig(bpy.types.Operator):
    bl_idname = "rigools.initialize_rig"
    bl_label = "Initialize Rig"
    bl_description = "Load all of the rig settings"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return {"FINISHED"}


class RIGTOOLS_set_turnaround_length(bpy.types.Operator):
    bl_idname = "rigools.set_pose_length"
    bl_label = "Set Turnaround Length"
    bl_description = "Set how many turnaround poses make up the character"
    bl_options = {"REGISTER", "UNDO"}

    pose_length_set: bpy.props.IntProperty(name="Turnaround Length")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column(align=True)
        lines = [
            "Turnaround Length effects how the turnaround pose ",
            "is interperted. Changing this will break compatibility",
            "with previous animations tracks.",
        ]
        for line in lines:
            col.alert = True
            col.label(text=line)
        col.label(text="Proceed with Caution!", icon="ERROR")
        col = self.layout.column()
        col.label(text="Use 'ESC' to cancel")
        if context.active_object.tiny_rig.pose_length:
            self.pose_length_set = context.active_object.tiny_rig.pose_length
        col.prop(self, "pose_length_set")

    def execute(self, context):
        context.active_object.tiny_rig.pose_length = self.pose_length_set
        return {"FINISHED"}


class RIGTOOLS_toggle_enable_action(bpy.types.Operator):
    @classmethod
    def poll(cls, context):
        return (
            context.active_object.animation_data.action
            != context.active_object.offset_action
            and context.active_object.mode == "POSE"
        )

    bl_idname = "rigools.enable_offset_action"
    bl_label = "Edit Offset Action"
    bl_description = "Enable Turnaround Offset Action Editor"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        if context.window_manager.offset_editor_active == True:
            self.report({"ERROR"}, "Offset Editor already Enabled")
            return {"CANCELLED"}
        offset_action = obj.offset_action
        if not offset_action:
            self.report({"ERROR"}, "Offset Action not Set")
            return {"CANCELLED"}
        if obj.mode != "POSE":
            self.report({"ERROR"}, "Must be in POSE Mode")
            return {"CANCELLED"}
        if obj.animation_data.action == offset_action:
            self.report({"ERROR"}, "Offset Action already Enabled")
            return {"CANCELLED"}
        if obj.animation_data and obj.animation_data.action:
            global old_action
            old_action = obj.animation_data.action

        obj.animation_data.action = None
        reset_bones(obj.pose.bones)
        constraints = get_action_offset_bones(obj.pose.bones)
        show_hide_constraints(constraints, False)
        obj.animation_data.action = offset_action
        context.window_manager.offset_editor_active = True
        self.report({"INFO"}, "Offset Editing Enabled!")
        return {"FINISHED"}


class RIGTOOLS_toggle_disable_action(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.disable_offset_action"
    bl_label = "Disable Offset Action Editing"
    bl_description = "Disable Turnaround Offset Action Editor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object.animation_data.action
            == context.active_object.offset_action
            and context.active_object.mode == "POSE"
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
        context.window_manager.offset_editor_active = False
        global old_action
        if old_action is not None:
            obj.animation_data.action = old_action
        self.report({"INFO"}, "Offset Editing Disabled!")
        return {"FINISHED"}


class RIGTOOLS_load_action(RIGTOOLS_rig_edit_base_class):
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
    bl_label = "Add Offset to Selected Bones"
    bl_description = """If a bone is included in the active_object's 'Offset Action' add constraint to move bone via action constraint. 
    This will also add a driver back to the Body/Head Poses"""
    bl_options = {"UNDO"}

    is_head: bpy.props.BoolProperty(
        name="Is Head",
        description="Set selected bone(s) as Head Turnaround and create a Head Pose Action Offset. Else Body Action Offset",
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        res = not (
            obj.library
            or obj.override_library
            or obj.animation_data.action == obj.offset_action
        )
        if not res:
            cls.poll_message_set("Cannot Edit while Offsetting Turnaround Action")
        return res

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop(self, "is_head")

    def execute(self, context):
        if self.is_head:
            add_action_const_to_head(context)
        else:
            add_action_const_to_body(context)
        return {"FINISHED"}


class RIGTOOLS_add_ik_mirror_to_pole(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_ik_mirror_to_pole"
    bl_label = "Add Flip to Pole Bone"
    bl_description = """Add Mirror Pole Transform Constraint to selected Bone"""
    bl_options = {"UNDO"}

    def execute(self, context):
        bone = context.active_pose_bone
        if "_Pole" not in bone.name:
            self.report({"ERROR"}, f"Active Bone must be Pole Target")
            return {"CANCELLED"}

        suffix = bone.name.split("_Pole")[0]
        if not get_consts_on_bone(bone, "TRANSFORM"):
            new = bone.constraints.new("TRANSFORM")
            new.target = context.active_object
            new.subtarget = f"{suffix}_Nudge"
            new.target_space = "LOCAL_WITH_PARENT"
            new.owner_space = "LOCAL_WITH_PARENT"
            new.to_min_y = -4.5
            add_driver(
                bone.id_data,
                bone.id_data,
                f"{suffix}_Flip_IK",
                f'pose.bones["{bone.name}"].constraints["{new.name}"].influence',
                f'pose.bones["PoseData"]["{suffix}_Flip_IK"]',
            )
        return {"FINISHED"}


class RIGTOOLS_add_hand_nudge(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_hand_nudge"
    bl_label = "Add Nudge to Hand Bone"
    bl_description = """Add Hand Nudge Constraint to selected Bone"""
    bl_options = {"UNDO"}

    def execute(self, context):

        bone = context.active_pose_bone
        if "_Arm.Hand" not in bone.name:
            self.report({"ERROR"}, f"Active Bone must be Hand")
            return {"CANCELLED"}
        if "HAND_NUDGE" in [const.name for const in bone.constraints]:
            self.report({"ERROR"}, f"Hand Nundge already exists on {bone.name}")
            return {"CANCELLED"}

        suffix = bone.name.split(".Hand")[0]
        side = suffix.split("_Arm")[0]
        new = bone.constraints.new("TRANSFORM")
        new.target = context.active_object
        new.subtarget = f"{suffix}_Nudge"
        new.target_space = "LOCAL"
        new.owner_space = "LOCAL"
        new.to_min_z = -0.05
        new.name = "HAND_NUDGE"
        add_driver(
            bone.id_data,
            bone.id_data,
            f"{side}_Hand_Nudge",
            f'pose.bones["{bone.name}"].constraints["{new.name}"].influence',
            f'pose.bones["PoseData"]["{side}_Hand_Nudge"]',
        )
        return {"FINISHED"}


class RIGTOOLS_add_mirror_to_bone(RIGTOOLS_rig_edit_base_class):
    bl_idname = "rigools.add_mirror_to_hand_foot_bone"
    bl_label = "Add Flip to Hand/Foot Bone"
    bl_description = """Add Hand Foot Mirror Constraint"""
    bl_options = {"UNDO"}

    def execute(self, context):
        bone = context.active_pose_bone
        if not (".Hand" in bone.name or ".Foot" in bone.name):
            self.report({"ERROR"}, f"Active Bone must be Hand or Foot")
            return {"CANCELLED"}
        if "FLIP_BONE" in [const.name for const in bone.constraints]:
            self.report({"ERROR"}, f"Hand Nundge already exists on {bone.name}")
            return {"CANCELLED"}

        prefix = bone.name[0]
        suffix = bone.name.split(".")[1]
        new = bone.constraints.new("TRANSFORM")
        new.target = context.active_object
        new.subtarget = f"{bone.name.split('.')[0]}_Nudge"
        new.target_space = "LOCAL_WITH_PARENT"
        new.owner_space = "LOCAL_WITH_PARENT"
        new.map_to = "ROTATION"
        new.to_min_y_rot = 3.1415927410125732
        new.name = "FLIP_BONE"
        add_driver(
            bone.id_data,
            bone.id_data,
            f"{prefix}_{suffix}_Flip",
            f'pose.bones["{bone.name}"].constraints["{new.name}"].influence',
            f'pose.bones["PoseData"]["{prefix}_{suffix}_Flip"]',
        )
        return {"FINISHED"}


class RIGTOOLS_apply_legacy_transforms(RIGTOOLS_rig_edit_base_class):
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


class RIGTOOLS_add_ik_fk_toggle(RIGTOOLS_rig_edit_base_class):
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
    RIGTOOLS_add_action_const_to_bone,
    RIGTOOLS_toggle_enable_action,
    RIGTOOLS_toggle_disable_action,
    RIGTOOLS_load_action,
    RIGTOOLS_set_turnaround_length,
    RIGTOOLS_initialize_rig,
    RIGTOOLS_add_ik_mirror_to_pole,
    RIGTOOLS_add_hand_nudge,
    RIGTOOLS_add_mirror_to_bone,
    RIGTOOLS_enter_grease_pencil_editor,
    RIGTOOLS_enter_grease_pencil_editor_exit,
    RIGTOOLS_isolate_gpencil,
    RIGTOOLS_enable_all_gp_mod_const,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
