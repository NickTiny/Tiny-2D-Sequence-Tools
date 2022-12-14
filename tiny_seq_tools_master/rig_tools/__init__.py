from tiny_seq_tools_master.rig_tools import rig_control, rig_editor


def register():
    rig_control.register()
    rig_editor.register()


def unregister():
    rig_control.unregister()
    rig_editor.unregister()
