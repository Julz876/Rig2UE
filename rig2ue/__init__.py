# rig2ue/__init__.py

bl_info = {
    "name": "Rig2UE - Rig Retargeter",
    "author": "KingxJulz",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Rig2UE",
    "description": "Convert custom Blender rigs to UE5, UE4, MetaHuman Skeletons.",
    "category": "Rigging",
}

import bpy
from .ui import rig2ue_panel, mapping_item,rig2ue_mapping_panel,rig2ue_export_panel, rig2ue_help_panel
from .ui.rig2ue_panel import get_armature_list
from .operators import (
    convert_rig_operator,
    refresh_mapping_operator,
    pose_corrector_operator,
    export_fbx_operator,
    save_preset_operator,
    load_preset_operator,
    full_pipeline_operator,
    mapping_editor_operator,


)

modules = (
    rig2ue_panel,
    rig2ue_mapping_panel,
    rig2ue_export_panel,
    rig2ue_help_panel,
    mapping_item,
    convert_rig_operator,
    refresh_mapping_operator,
    pose_corrector_operator,
    export_fbx_operator,
    save_preset_operator,
    load_preset_operator,
    full_pipeline_operator,
    mapping_editor_operator,
)

class Rig2UEProperties(bpy.types.PropertyGroup):
    source_armature: bpy.props.EnumProperty(
        name="Source Armature",
        items=get_armature_list
    )
    
    target_profile: bpy.props.EnumProperty(
        name="Target Profile",
        items=[
            ('UE5', "UE5 Skeleton", ""),
            ('UE4', "UE4 Skeleton", ""),
            ('METAHUMAN', "MetaHuman Skeleton", ""),
            ('BLENDER_METARIG', "Blender MetaRig", ""),
            ('UEFORMAT', "Fmodel UE Format", ""),
            ('PSK', "ActorX", "")
        ],
        default='UE5'
    )

    mapping_preview: bpy.props.CollectionProperty(type=mapping_item.Rig2UE_MappingItem)

    export_folder: bpy.props.StringProperty(
        name="Export Folder",
        subtype='DIR_PATH',
        default="//",
    )
    export_filename: bpy.props.StringProperty(
        name="File Name",
        default="exported_rig",
    )
    enable_advanced_mode: bpy.props.BoolProperty(
        name="Enable Advanced Mode",
        description="Show advanced options and controls",
        default=False
    )
    show_mapping_list: bpy.props.BoolProperty(
    name="Show Mapping List",
    default=True,
)


class Rig2UEAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    default_export_folder: bpy.props.StringProperty(
        name="Default Export Folder",
        subtype='DIR_PATH',
        default="//exports/"
    )

    default_export_filename: bpy.props.StringProperty(
        name="Default Export File Name",
        default="exported_rig"
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Rig2UE Export Defaults:")
        layout.prop(self, "default_export_folder")
        layout.prop(self, "default_export_filename")


def register():
    for module in modules:
        module.register()
    bpy.utils.register_class(Rig2UEProperties)
    bpy.utils.register_class(Rig2UEAddonPreferences)
    bpy.types.Scene.rig2ue_props = bpy.props.PointerProperty(type=Rig2UEProperties)

def unregister():
    for module in reversed(modules):
        module.unregister()
    bpy.utils.unregister_class(Rig2UEProperties)
    bpy.utils.unregister_class(Rig2UEAddonPreferences)
    del bpy.types.Scene.rig2ue_props


if __name__ == "__main__":
    register()
