import bpy

from tiny_seq_tools_master.scene_strip_tools.core import make_render_scene
from bpy.props import StringProperty

class SEQUENCER_rename_scene_strips(bpy.types.Operator):
    bl_idname = "sequencer.renmae_strips"
    bl_label = "Rename Scene Strips"
    bl_description = "Set a new name for scene strips, add prefixes in the order they appear in timeline."

    prefix : bpy.props.StringProperty(name="Name Pefix", description="prefix to add to renamed scene strips, followed a number", default="SH")
    suffix_length : bpy.props.IntProperty(name="Number Length", description="Length of number to follow prefix", default=4)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
       self.layout.label(text="Rename all strips to '{Prefix}0010'")
       self.layout.prop(self,"prefix" )
       self.layout.prop(self,"suffix_length" )
       
    
    def execute(self, context):
        sequences = [strip for strip in context.scene.sequence_editor.sequences_all if strip.type =="SCENE"]
        sequences_sorted = sorted(sequences, key=lambda x: x.frame_final_start)
        for index, seq in enumerate(sequences_sorted):
           
            index = str((index+1)*10)
            seq.name = f"{self.prefix}{index.zfill(self.suffix_length)}"
        return {'FINISHED'}
    
class SEQUENCER_preview_render(bpy.types.Operator):
    bl_idname = "sequencer.preview_render"
    bl_label = "Render Preview Video"
    bl_description = "Render sequencer preview video from the viewport. Will always produce .mov files."

    first_mouse_x = bpy.props.IntProperty()
    first_value = bpy.props.FloatProperty()

    def execute(self, context):
        if context.scene.name == "RENDER":
            self.report({"ERROR"}, "Render scene cannot be active")
            return {"CANCELLED"}

        render_scene = make_render_scene(context)
        render_scene.render.engine = 'BLENDER_WORKBENCH'
        wm = context.window_manager
        render_scene = bpy.data.scenes["RENDER"]
        render_scene.render.image_settings.file_format = "FFMPEG"
        render_scene.render.ffmpeg.codec = "H264"
        render_scene.render.ffmpeg.audio_codec = "AAC"
        render_scene.render.filepath = render_scene.render.filepath+"_preview_.mov"
        if wm.render_settings.render_preview_range:
            render_scene.frame_start = wm.render_settings.render_start
            render_scene.frame_end = wm.render_settings.render_end
        user_scene = context.window.scene
        context.window.scene = render_scene
        bpy.ops.render.opengl(animation=True, sequencer=True,)
        self.report({"INFO"}, f"Full Render Complete")
        context.window.scene = user_scene
        return {"FINISHED"}


class SEQUENCER_setup_render(bpy.types.Operator):
    bl_idname = "sequencer.setup_render"
    bl_label = "Setup Render Scene"
    bl_description = "Build Render Scene based on current Scene Settings"

    def execute(self, context):
        if context.scene.name == "RENDER":
            self.report({"ERROR"}, "Render scene cannot be active")
            return {"CANCELLED"}
        make_render_scene(context)

        self.report({"INFO"}, f"Render Scene has been setup")
        return {"FINISHED"}


class SEQUENCER_full_render(bpy.types.Operator):
    bl_idname = "sequencer.full_render_legacy"
    bl_label = "Render Scene"
    bl_description = "Render a sequencer video using Blender's native render. Will always match scene render settings."

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.label(text="Full Renders can be slow.")
        self.layout.label(text="Are you sure you want to proceed?")

    def execute(self, context):
        import bpy
        wm = bpy.context.window_manager
        tot = 1000
        wm.progress_begin(0, tot)
        wm.progress_update(25)
        if context.scene.name == "RENDER":
            self.report({"ERROR"}, "Render scene cannot be active")
            return {"CANCELLED"}
        render_scene = make_render_scene(context)
        user_scene = context.window.scene
        context.window.scene = render_scene
        render_scene.render.use_sequencer = True
        bpy.ops.render.render(animation=True,)
        wm.progress_update(50)
        self.report({"INFO"}, f"Full Render Complete")
        context.window.scene = user_scene
        wm.progress_end()
        return {"FINISHED"}


class SEQUENCER_add_camera_from_view(bpy.types.Operator):
    bl_idname = "sequencer.add_camera_from_view"
    bl_label = "Add Camera from Current View"
    bl_description = "Add Camera to active sequence strip based on viewport camera"
    bl_context = "VIEW_3D"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        camera_name = "NEW CAMERA"
        camera_data = bpy.data.cameras.new(camera_name)
        camera_obj = bpy.data.objects.new(f"{camera_name}", camera_data)
        context.scene.collection.objects.link(camera_obj)
        context.scene.camera = bpy.data.objects[camera_name]
        bpy.ops.view3d.camera_to_view("INVOKE_DEFAULT")
        return {"FINISHED"}


class SEQUENCER_check_viewport_sync_errors(bpy.types.Operator):
    bl_idname = "sequencer.check_viewport_sync_errors"
    bl_label = "Check for Sync Errors"
    bl_description = "Check if Sequence's Strips have 'Hold Offset Start' greater than one and report as an error. \n If true, these strips will not appear in 'sync' during render"

    def execute(self, context):
        error_msg = ""
        for strip in context.scene.sequence_editor.sequences_all:
            if strip.type == "SCENE" and not strip.mute:
                if strip.animation_offset_start != 0:
                    error_msg += f"'{strip.name}' is out of sync. Frames: ({strip.frame_final_start}, {strip.frame_final_end})"
                    
        if error_msg != "":
            self.report(
                {"ERROR"},
                f"Strips are out of sync, render animation will not match viewport \n {error_msg}",
            )
            return {"CANCELLED"}
        self.report({"INFO"}, f"All Strips are in sync")
        return {"FINISHED"}
    
class SEQUENCER_fix_viewport_sync_errors(bpy.types.Operator):
    bl_idname = "sequencer.fix_viewport_sync_errors"
    bl_label = "Fix Sync Errors"
    bl_description = "Fix Sync Errors will re-generate all scene strips to ensure they are in sync"
    def execute(self, context):
        sequences = context.scene.sequence_editor.sequences
        source_strips = [strip for strip in sequences if strip.type == "SCENE"]

        for source_strip in source_strips:
            channel = source_strip.channel
            scene = source_strip.id_data
            source_strip.mute = True
            new_strip = scene.sequence_editor.sequences.new_scene("Scene", bpy.context.scene, channel+1, scene.frame_start)
            source_strip.name = f"old_{source_strip.name}"
            new_strip.name = source_strip.name.replace("old_","")
            new_strip.frame_final_start = source_strip.frame_final_start
            new_strip.frame_final_end = source_strip.frame_final_end
            new_strip.scene_input = source_strip.scene_input
            new_strip.scene_camera = source_strip.scene_camera
            scene.sequence_editor.sequences.remove(source_strip)
            new_strip.channel = channel
            
        return {"FINISHED"}

class SEQUENCER_refresh_viewport_camera(bpy.types.Operator):
    bl_idname = "sequencer.refresh_viewport_camera"
    bl_label = "Refresh Viewport Camera"
    bl_description = "Refresh Viewport after changing the camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        cur_frame = context.scene.frame_current_final
        end_of_strip = context.active_sequence_strip.frame_final_end
        context.scene.frame_set(end_of_strip + 1)
        context.scene.frame_set(int(cur_frame))
        self.report({"INFO"}, "Viewport Refreshed")
        return {"FINISHED"}


class SEQUENCER_OT_add_scene_strip(bpy.types.Operator):

    bl_description = """Adds current camera as a scene strip to the Sequencer"""
    bl_idname = "view3d.add_scene_strip"
    bl_label = "Camera"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):

        if not bpy.context.scene.sequence_editor:
            bpy.context.scene.sequence_editor_create()
            self.report(
                {"INFO"}, f"New Sequence Editor cerated in '{scn.name}'")
        scn = bpy.context.scene
        seq = scn.sequence_editor
        cf = scn.frame_current
        addSceneOut = scn.frame_end
        addSceneChannel = 2
        addSceneTlStart = cf
        newScene = seq.sequences.new_scene(
            "Scene", bpy.context.scene, addSceneChannel, addSceneTlStart
        )
        seq.sequences_all[newScene.name].scene_camera = bpy.data.objects[
            bpy.context.scene.camera.name
        ]
        seq.sequences_all[newScene.name].frame_final_end = addSceneOut
        seq.sequences_all[newScene.name].frame_start = cf
        self.report({"INFO"}, f"'{newScene.name}' added to '{scn.name}'")
        return {"FINISHED"}


classes = (
    SEQUENCER_OT_add_scene_strip,
    SEQUENCER_add_camera_from_view,
    SEQUENCER_full_render,
    SEQUENCER_setup_render,
    SEQUENCER_preview_render,
    SEQUENCER_check_viewport_sync_errors,
    SEQUENCER_fix_viewport_sync_errors,
    SEQUENCER_refresh_viewport_camera,
    SEQUENCER_rename_scene_strips,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
