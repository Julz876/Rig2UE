import bpy
from ..utils import auto_mapper
from ..utils import bone_mapping_profiles

class Rig2UE_OT_RefreshMapping(bpy.types.Operator):
    bl_idname = "rig2ue.refresh_mapping"
    bl_label = "Refresh Mapping"
    bl_description = "⚠️ Warning: This will overwrite your manual edits."

    def execute(self, context):
        scene = context.scene
        rig2ue_props = scene.rig2ue_props

        source_rig_name = rig2ue_props.source_armature
        target_profile_key = rig2ue_props.target_profile

        source_rig = bpy.data.objects.get(source_rig_name)
        if not source_rig:
            self.report({'ERROR'}, "Selected rig not found.")
            return {'CANCELLED'}

        profile = bone_mapping_profiles.PROFILES.get(target_profile_key)
        if not profile:
            self.report({'ERROR'}, "Target profile not found.")
            return {'CANCELLED'}

        # Refresh bone mapping
        bone_map = auto_mapper.map_bones(source_rig, profile)

        rig2ue_props.mapping_preview.clear()
        for target_bone, source_bone in bone_map.items():
            item = rig2ue_props.mapping_preview.add()
            item.target_bone = target_bone
            item.source_bone = source_bone if source_bone else ""

        self.report({'INFO'}, "Mapping refreshed successfully.")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

def register():
    bpy.utils.register_class(Rig2UE_OT_RefreshMapping)

def unregister():
    bpy.utils.unregister_class(Rig2UE_OT_RefreshMapping)
