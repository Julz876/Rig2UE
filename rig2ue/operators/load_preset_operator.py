import bpy
import os
from ..utils import mapping_preset_manager

class Rig2UE_OT_LoadMappingPreset(bpy.types.Operator):
    bl_idname = "rig2ue.load_mapping_preset"
    bl_label = "Load Mapping Preset"
    bl_description = "Load a saved bone mapping preset."

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        scene = context.scene
        rig2ue_props = scene.rig2ue_props

        filename = os.path.basename(self.filepath)
        mapping_preset_manager.load_mapping_preset(rig2ue_props, filename)

        self.report({'INFO'}, f"Loaded preset: {filename}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(Rig2UE_OT_LoadMappingPreset)

def unregister():
    bpy.utils.unregister_class(Rig2UE_OT_LoadMappingPreset)
