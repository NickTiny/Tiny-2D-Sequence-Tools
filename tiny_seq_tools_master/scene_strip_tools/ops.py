import bpy

from tiny_seq_tools_master.scene_strip_tools.core import make_render_scene

from lib2to3.pgen2.token import STAREQUAL
import bpy
import mathutils
from mathutils import Matrix
from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty, EnumProperty
from bpy.types import Panel, Menu
from rna_prop_ui import PropertyPanel
from operator import attrgetter


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
        return {"FINISHED"}


class SEQUENCER_setup_render(bpy.types.Operator):
    bl_idname = "sequencer.setup_render"
    bl_label = "Setup Render Scene"
    bl_description = ""

    def execute(self, context):
        if context.scene.name == "RENDER":
            self.report({"ERROR"}, "Render scene cannot be active")
            return {"CANCELLED"}
        make_render_scene(context)

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
        return {"FINISHED"}


class THREEDPREVIEW_PT_add_scene_strip(bpy.types.Operator):
    """Adds current camera as a scene strip to the Sequencer"""

    bl_idname = "view3d.add_scene_strip"
    bl_label = "Camera"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):

        if not bpy.context.scene.sequence_editor:
            bpy.context.scene.sequence_editor_create()
        scn = bpy.context.scene
        seq = scn.sequence_editor
        cf = scn.frame_current
        addSceneIn = cf
        addSceneOut = scn.frame_end
        addSceneChannel = 2
        addSceneTlStart = cf
        newScene = seq.sequences.new_scene(
            "Scene", bpy.context.scene, addSceneChannel, addSceneTlStart
        )
        seq.sequences_all[newScene.name].scene_camera = bpy.data.objects[
            bpy.context.scene.camera.name
        ]
        seq.sequences_all[newScene.name].animation_offset_start = addSceneIn
        seq.sequences_all[newScene.name].frame_final_end = addSceneOut
        seq.sequences_all[newScene.name].frame_start = cf

        return {"FINISHED"}


class SEQUENCE_PT_convert_cameras(bpy.types.Operator):
    """Converts 'Bind Camera To Markers' to Scene Strips"""

    bl_label = "Convert Camera Markers"
    bl_idname = "sequencer.convert_cameras"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = bpy.context.scene

        if not bpy.context.scene.sequence_editor:  # create sequence, if missing
            bpy.context.scene.sequence_editor_create()

        marker_camera = []
        marker_frame = []
        marker_name = []
        cam_marker = []
        cnt = 0
        mi = bpy.context.scene.timeline_markers.items()
        for marker in scene.timeline_markers:  # find the cameras and their frame

            if marker.camera:
                cam_marker.insert(
                    cnt, [marker.frame, marker.camera.name]
                )  # mi[cnt][0]])
                cnt += 1

        if len(cam_marker) == 0:  # cancel if no cameras
            return {"CANCELLED"}

        cam_marker = sorted(
            cam_marker, key=lambda mark: mark[0]
        )  # Sort the markers after frame nr.

        # add cameras to sequencer
        cnt = 0  # counter
        for i in cam_marker:
            cf = cam_marker[cnt][0]
            addSceneIn = cf

            if cnt < len(cam_marker) - 1:  # find out frame
                addSceneOut = cam_marker[cnt + 1][0]
            else:
                addSceneOut = (
                    addSceneIn + 151
                )  # last clip extented 30 fps*5 frames + an ekstra frame for the hack.
                bpy.context.scene.frame_end = (
                    addSceneIn + 150
                )  # extent preview area or add scene strip may fail

            addSceneChannel = 1  # attempt to add in this channel - if full, strips will be moved upwards
            addSceneTlStart = cf

            # Hack: adding a scene strip will make a hard cut one frame before preview area end.
            bpy.context.scene.frame_end = bpy.context.scene.frame_end + 1

            # add scene strip in current scene at in and out frame numbers
            newScene = bpy.context.scene.sequence_editor.sequences.new_scene(
                cam_marker[cnt][1], bpy.context.scene, addSceneChannel, addSceneTlStart
            )
            newScene.scene_camera = bpy.data.objects[cam_marker[cnt][1]]
            newScene = bpy.context.scene.sequence_editor.sequences_all[newScene.name]
            newScene.animation_offset_start = addSceneIn
            newScene.frame_final_end = addSceneOut
            newScene.frame_start = cf
            cnt += 1

            # Hack: remove the extra frame again of the preview area.
            bpy.context.scene.frame_end = bpy.context.scene.frame_end - 1

        return {"FINISHED"}


# class SEQUENCER_OT_scene_change(bpy.types.Operator):
class values:
    prev_scene_change = ""


class SEQUENCER_OT_scene_change(bpy.types.Operator):

    """Change scene to active strip scene"""

    bl_idname = "sequencer.change_scene"
    bl_label = "Toggle Scene Strip"
    bl_description = "Change scene to active strip scene"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(self, context):
        if context.scene:
            return True
        else:
            return False

    def act_strip(context):
        try:
            return context.scene.sequence_editor.active_strip
        except AttributeError:
            return False

    def execute(self, context):
        if not bpy.context.scene.sequence_editor:
            bpy.context.scene.sequence_editor_create()
        strip = self.act_strip(context)
        scene = bpy.context.scene
        sequence = scene.sequence_editor

        if strip != None:  # save camera
            if strip.type == "SCENE":
                if (
                    sequence.sequences_all[strip.name].scene_input == "CAMERA"
                    and strip.scene_camera != None
                ):
                    camera = strip.scene_camera.name

        if strip == None:  # no active strip
            if values.prev_scene_change != "":  # a previous scene - go back
                win = bpy.context.window_manager.windows[0]
                win.scene = bpy.data.scenes[values.prev_scene_change]
                return {"FINISHED"}
            elif values.prev_scene_change == "":  # no previous - do nothing
                return {"FINISHED"}

        else:  # an active strip exists

            if (
                strip.type != "SCENE" and values.prev_scene_change != ""
            ):  # wrong strip type, but a previous scene - go back
                win = bpy.context.window_manager.windows[0]
                win.scene = bpy.data.scenes[values.prev_scene_change]

            elif strip.type == "SCENE":  # correct strip type
                strip_scene = bpy.context.scene.sequence_editor.active_strip.scene.name
                values.prev_scene_change = scene.name

                # scene strip in 'Camera' and a camera is selected

                if (
                    sequence.sequences_all[strip.name].scene_input == "CAMERA"
                    and strip.scene_camera != None
                ):
                    for area in bpy.context.screen.areas:
                        if area.type == "VIEW_3D":
                            win = bpy.context.window_manager.windows[0]
                            win.scene = bpy.data.scenes[strip_scene]
                            bpy.context.scene.camera = bpy.data.objects[
                                camera
                            ]  # select camera as view
                            area.spaces.active.region_3d.view_perspective = (
                                "CAMERA"  # use camera view
                            )

                else:  # no scene strip in 'Camera' mode or a camera may not be selected

                    strip_scene = (
                        bpy.context.scene.sequence_editor.active_strip.scene.name
                    )
                    values.prev_scene_change = scene.name
                    win = bpy.context.window_manager.windows[0]
                    win.scene = bpy.data.scenes[strip_scene]

        return {"FINISHED"}


classes = (
    THREEDPREVIEW_PT_add_scene_strip,
    SEQUENCE_PT_convert_cameras,
    SEQUENCER_OT_scene_change,
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
