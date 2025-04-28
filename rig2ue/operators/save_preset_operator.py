import bpy
from ..utils import mapping_preset_manager

class Rig2UE_OT_SaveMappingPreset(bpy.types.Operator):
    bl_idname = "rig2ue.save_mapping_preset"
    bl_label = "Save Mapping Preset"
    bl_description = "Save current bone mapping as a preset."

    preset_name: bpy.props.StringProperty(name="Preset Name", default="my_mapping")

    def execute(self, context):
        scene = context.scene
        rig2ue_props = scene.rig2ue_props

        filename = f"{self.preset_name}.json"
        mapping_preset_manager.save_mapping_preset(rig2ue_props, filename)

        self.report({'INFO'}, f"Saved preset: {filename}")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(Rig2UE_OT_SaveMappingPreset)

def unregister():
    bpy.utils.unregister_class(Rig2UE_OT_SaveMappingPreset)
