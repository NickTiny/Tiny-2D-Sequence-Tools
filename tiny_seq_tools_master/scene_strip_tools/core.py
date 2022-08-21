import string
import bpy


def set_active_sequence_strip(strip: bpy.types.Sequence) -> bool:
    """Set active strip to given strip"""
    scene = strip.id_data
    if scene.selection_to_active:
        scene.sequence_editor.active_strip = strip
        return True
    return False


## TODO Build context better here
def sync_strip_camera_to_viewport(strip: bpy.types.Sequence) -> bool:
    """Set avaliable viewports to strip's camera"""
    updated_viewport = False
    scene = strip.id_data
    if not scene.link_seq_to_3d_view:
        updated_viewport = False
        return updated_viewport
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            bpy.context.scene.camera = bpy.data.objects[
                strip.scene_camera.name
            ]  # Select camera as view
            area.spaces.active.region_3d.view_perspective = "CAMERA"  # Use camera view
            updated_viewport = True
    return updated_viewport


def make_render_scene(context: bpy.types.Context) -> (bpy.types.Scene):
    """Create Scene called 'RENDER' from current scene settings, and copy all strips into it."""
    scene_name = "RENDER"
    user_scene_name = str(context.scene.name)
    for scene in bpy.data.scenes:
        if scene.name == scene_name:
            bpy.ops.scene.delete({"scene": bpy.data.scenes[scene_name]})

    bpy.ops.scene.new("INVOKE_DEFAULT", type="EMPTY")
    bpy.context.scene.sequence_editor_create()
    bpy.context.scene.name = scene_name
    render_scene = bpy.data.scenes[scene_name]
    context.window.scene = bpy.data.scenes[f"{user_scene_name}"]

    # Copy Strips
    context.scene.frame_set(1)
    bpy.ops.sequencer.select_all(action="SELECT")
    bpy.ops.sequencer.copy()

    # Paste Strips
    context.window.scene = render_scene
    context.scene.frame_set(1)
    bpy.ops.sequencer.paste()
    context.window.scene = bpy.data.scenes[f"{user_scene_name}"]
    return render_scene


def get_scene_strip_cameras(scene):
    return sorted(
        (
            obj
            for obj in scene
            if obj.type == "CAMERA" and obj.name != scene.line_art_cam_name
        ),
        key=lambda x: x.name,
    )
