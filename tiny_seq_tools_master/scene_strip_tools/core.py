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
    bpy.context.scene.camera = bpy.data.objects[
        strip.scene_camera.name
    ]  # Select camera as view
    updated_viewport = True
    return updated_viewport


def make_render_scene(context: bpy.types.Context) -> (bpy.types.Scene):
    """Create Scene called 'RENDER' from current scene settings, and copy all strips into it"""
    scene_name = "RENDER"
    user_scene = context.scene

    for scene in bpy.data.scenes:
        if scene.name == scene_name:
            bpy.ops.scene.delete({"scene": bpy.data.scenes[scene_name]})
    bpy.context.view_layer.update()

    render_scene = context.scene.copy()
    render_scene.name = scene_name
    render_scene.use_fake_user = False

    for strip in render_scene.sequence_editor.sequences_all:
        if strip.type == "SCENE":
            strip.scene = user_scene

    for col in render_scene.collection.children:
        render_scene.collection.children.unlink(col)
    for obj in render_scene.collection.objects:
        render_scene.collection.objects.unlink(obj)

    for collection in render_scene.collection.children:
        scene.collection.children.unlink(collection)

    render_scene.render.use_sequencer = True

    context.window.scene = user_scene
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
