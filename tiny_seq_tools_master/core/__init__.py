from tiny_seq_tools_master.core import save_pre, sync_core


def register():
    sync_core.register()
    save_pre.register()


def unregister():
    sync_core.unregister()
    save_pre.unregister()
