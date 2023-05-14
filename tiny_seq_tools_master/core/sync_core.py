import bpy
from typing import Union
from tiny_seq_tools_master.constraint_to_cams.core import constraints_to_active_camera
from tiny_seq_tools_master.line_art_tools.core import sync_strip_camera_to_seq_line_art
from tiny_seq_tools_master.scene_strip_tools.core import (
    sync_strip_camera_to_viewport,
    set_active_sequence_strip,
)

# Borrowed from https://github.com/The-SPA-Studios/sequencer-addon

OldStrip = ""


def remap_frame_value(frame: int, scene_strip: bpy.types.SceneSequence) -> int:
    """Remap `frame` in `scene_strip`'s underlying scene reference.

    :param frame: The frame to remap
    :param scene_strip: The scene strip to remap to.
    :returns: The remapped frame value
    """
    return int(frame - scene_strip.frame_start + scene_strip.scene.frame_start)

def get_strips_at_frame(
    frame: int,
    strips: list[bpy.types.Sequence],
    type_filter,
    skip_muted: bool = True,
) -> list[bpy.types.Sequence]:
    """
    Get all strips containing the given `frame` within their final range.

    :param frame: The frame value
    :param strips: The strips to consider
    :param type_filter: Only consider strips that are instances of the given type(s)
    :param skip_muted: Whether to skip muted strips
    :returns: The subset of strips matching the given parameters
    """
    return [
        s
        for s in strips
        if (
            (not type_filter or isinstance(s, type_filter))
            and (not skip_muted or not s.mute)
            and (frame >= s.frame_final_start and frame < s.frame_final_end)
        )
    ]


def get_scene_strip_at_frame(
    frame: int,
    sequence_editor: bpy.types.SequenceEditor,
    skip_muted: bool = True,
) -> tuple[Union[bpy.types.SceneSequence, None], int]:
    """
    Get the scene strip at `frame` in `sequence_editor`'s strips with the highest
    channel number.

    :param frame: The frame value
    :param sequence_editor: Sequence editor containing the strips
    :param skip_muted: Exclude muted strips
    :returns: The scene strip (or None) and the frame in underlying scene's reference
    """
    
    strips = sequence_editor.sequences
    channels = sequence_editor.channels

    if skip_muted:
        # Exclude strips from muted channels
        muted_channels = [idx for idx, channel in enumerate(channels) if channel.mute]
        strips = [strip for strip in strips if not strip.channel in muted_channels]

    strips = get_strips_at_frame(frame, strips, bpy.types.SceneSequence, skip_muted)

    if not strips:
        return None, frame
    # Sort strips by channel
    strip = sorted(strips, key=lambda x: x.channel)[-1]

    # Help type checking: strip can only be a SceneSequence here
    assert isinstance(strip, bpy.types.SceneSequence)

    # Only consider scene strips with a valid scene
    if not strip.scene:
        return None, frame

    # Compute frame in underlying scene's reference
    return strip, remap_frame_value(frame, strip)


def update_constraint_camera(master_scene):
    global OldStrip
    if (not master_scene
        or not master_scene.sequence_editor
    ):
        return

    new_strip, _ = get_scene_strip_at_frame(
            master_scene.frame_current,
            master_scene.sequence_editor,
        )

    # No strip is available: stop here.
    if new_strip is None:
        return
    constraints_to_active_camera(new_strip)
    sync_strip_camera_to_seq_line_art(new_strip)
    if master_scene.name != "RENDER":  # Only if current scene in scene-strip
        sync_strip_camera_to_viewport(new_strip)
        set_active_sequence_strip(new_strip)
        OldStrip = new_strip.name
        return
    
    

@bpy.app.handlers.persistent
def constraint_to_camera_handler(self, context):
    update_constraint_camera(self)


def register():
    bpy.app.handlers.frame_change_pre.append(constraint_to_camera_handler)


def unregister():
    bpy.app.handlers.frame_change_pre.remove(constraint_to_camera_handler)
