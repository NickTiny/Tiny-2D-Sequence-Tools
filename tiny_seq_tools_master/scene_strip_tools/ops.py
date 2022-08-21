import bpy

from tiny_seq_tools_master.scene_strip_tools.core import make_render_scene
from bpy.props import StringProperty


class SEQUENCER_preview_render(bpy.types.Operator):
    bl_idname = "sequencer.preview_render"
    bl_label = "Render Preview Video"
    bl_description = "Render sequencer preview video from the viewport. Will always produce .mov files."

    first_mouse_x = bpy.props.IntProperty()
    first_value = bpy.props.FloatProperty()

    def execute(self, context):
        make_render_scene(context)
        wm = context.window_manager
        render_scene = bpy.data.scenes["RENDER"]
        render_scene.render.image_settings.file_format = "FFMPEG"
        render_scene.render.ffmpeg.codec = "H264"
        render_scene.render.ffmpeg.audio_codec = "AAC"
        render_scene = bpy.data.scenes["RENDER"]
        context.window.scene = render_scene
        bpy.ops.render.opengl("INVOKE_DEFAULT", animation=True, sequencer=True)
        self.report({"INFO"}, f"Preview Render Complete")
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
    bl_idname = "sequencer.batch_render"
    bl_label = "Render Scene"
    bl_description = "Render a sequencer video using Blender's native render. Will always match scene render settings."

    def execute(self, context):
        if context.scene.name != "RENDER":
            self.report({"ERROR"}, "Render scene must be active")
            return {"CANCELLED"}
        bpy.ops.render.render("INVOKE_DEFAULT", animation=True)
        self.report({"INFO"}, f"Full Render Complete")
        return {"FINISHED"}


class SEQUENCER_add_camera_from_view(bpy.types.Operator):
    bl_idname = "sequencer.add_camera_from_view"
    bl_label = "Add Camera from Current View"
    bl_description = "Add Camera to active sequence strip based on viewport camera"
    bl_context = "VIEW_3D"

    def execute(self, context):
        camera_name = "NEW CAMERA"
        camera_data = bpy.data.cameras.new(camera_name)
        camera_obj = bpy.data.objects.new(f"{camera_name}", camera_data)
        context.scene.collection.objects.link(camera_obj)
        context.scene.camera = bpy.data.objects[camera_name]
        bpy.ops.view3d.camera_to_view("INVOKE_DEFAULT")
        return {"FINISHED"}


class THREEDPREVIEW_PT_add_scene_strip(bpy.types.Operator):

    bl_description = """Adds current camera as a scene strip to the Sequencer"""
    bl_idname = "view3d.add_scene_strip"
    bl_label = "Camera"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):

        if not bpy.context.scene.sequence_editor:
            bpy.context.scene.sequence_editor_create()
            self.report({"INFO"}, f"New Sequence Editor cerated in '{scn.name}'")
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
    THREEDPREVIEW_PT_add_scene_strip,
    SEQUENCER_add_camera_from_view,
    SEQUENCER_full_render,
    SEQUENCER_setup_render,
    SEQUENCER_preview_render,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
