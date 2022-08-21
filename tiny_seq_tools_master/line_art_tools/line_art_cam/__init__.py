"""The Line Art Cam folder is made to cover a bug in line art, some of the code is not ideal but servicable until the bug is patched.
The Bug is that Line Art won't render from custom cameras so a new camera needs to be created and copy all it's keyframes to that. 
In this module this is referred to by override camera or just line art camera"""

from tiny_seq_tools_master.line_art_tools.line_art_cam import ops, props


def register():
    ops.register()
    props.register()


def unregister():
    ops.unregister()
    props.unregister()
