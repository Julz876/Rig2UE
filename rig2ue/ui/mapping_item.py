import bpy

class Rig2UE_MappingItem(bpy.types.PropertyGroup):
    target_bone: bpy.props.StringProperty(name="Target Bone")
    source_bone: bpy.props.StringProperty(name="Source Bone")

def register():
    bpy.utils.register_class(Rig2UE_MappingItem)

def unregister():
    bpy.utils.unregister_class(Rig2UE_MappingItem)
