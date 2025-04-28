import bpy

class Rig2UE_PT_ExportPanel(bpy.types.Panel):
    bl_label = "Rig2UE Export Settings"
    bl_idname = "RIG2UE_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rig2UE'

    def draw(self, context):
        layout = self.layout
        rig2ue_props = context.scene.rig2ue_props

        layout.prop(rig2ue_props, "export_folder")
        layout.prop(rig2ue_props, "export_filename")

        layout.separator()
        layout.label(text="Export Options:")
        layout.operator("rig2ue.export_fbx", text="Export UE FBX", icon='EXPORT')
        layout.operator("rig2ue.full_pipeline", text="One-Click Full Export", icon='FILE_TICK')
        layout.operator("rig2ue.reset_export_defaults", text="Reset to Defaults", icon='FILE_REFRESH')

def register():
    bpy.utils.register_class(Rig2UE_PT_ExportPanel)

def unregister():
    bpy.utils.unregister_class(Rig2UE_PT_ExportPanel)
