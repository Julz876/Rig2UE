import bpy

from ..utils import auto_mapper
from ..utils import bone_mapping_profiles
from ..utils import armature_builder, weight_transfer

class Rig2UE_OT_ConvertRig(bpy.types.Operator):
    bl_idname = "rig2ue.convert_rig"
    bl_label = "Convert Rig to Target Profile"
    bl_description = "Convert the selected armature to the chosen Unreal Engine skeleton profile."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        rig2ue_props = scene.rig2ue_props

        source_rig_name = rig2ue_props.source_armature
        target_profile_key = rig2ue_props.target_profile

        if not source_rig_name:
            self.report({'ERROR'}, "No source rig selected.")
            return {'CANCELLED'}

        source_rig = bpy.data.objects.get(source_rig_name)
        if not source_rig:
            self.report({'ERROR'}, "Selected rig not found in scene.")
            return {'CANCELLED'}

        profile = bone_mapping_profiles.PROFILES.get(target_profile_key)
        if not profile:
            self.report({'ERROR'}, "Target profile not found.")
            return {'CANCELLED'}

        # Check if user already manually edited
        if not rig2ue_props.mapping_preview:
            # Only auto-map if mapping is empty
            bone_map = auto_mapper.map_bones(source_rig, profile)

            rig2ue_props.mapping_preview.clear()
            for target_bone, source_bone in bone_map.items():
                item = rig2ue_props.mapping_preview.add()
                item.target_bone = target_bone
                item.source_bone = source_bone if source_bone else ""

        # Always use existing rig2ue_props.mapping_preview
        target_rig = armature_builder.build_target_armature(context, rig2ue_props)

        if target_rig:
            self.report({'INFO'}, "New UE Target Rig created successfully!")
        else:
            self.report({'ERROR'}, "Failed to create Target Rig.")

        return {'FINISHED'}


def check_incomplete_mapping(rig2ue_props):
    missing = []
    for mapping in rig2ue_props.mapping_preview:
        if not mapping.source_bone:
            missing.append(mapping.target_bone)
    return missing


def register():
    bpy.utils.register_class(Rig2UE_OT_ConvertRig)

def unregister():
    bpy.utils.unregister_class(Rig2UE_OT_ConvertRig)
