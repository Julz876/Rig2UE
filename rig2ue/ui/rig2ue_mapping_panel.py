import bpy

class Rig2UE_PT_MappingPanel(bpy.types.Panel):
    bl_label = "Rig2UE Mapping Settings"
    bl_idname = "RIG2UE_PT_mapping_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rig2UE'

    def draw(self, context):
        layout = self.layout
        rig2ue_props = context.scene.rig2ue_props

        layout.label(text="Mapping Presets:")
        row = layout.row(align=True)
        row.operator("rig2ue.save_mapping_preset", text="Save Preset", icon='PLUS')
        row.operator("rig2ue.load_mapping_preset", text="Load Preset", icon='IMPORT')

        layout.separator()
        layout.label(text="Bone Mapping Preview:")

        layout.separator()
        layout.operator("rig2ue.mapping_editor", text="Open Mapping Editor", icon='MODIFIER')

        layout.prop(rig2ue_props, "show_mapping_list", text="Show Mapping List", toggle=True)

        if rig2ue_props.show_mapping_list:
            box = layout.box()
            if not rig2ue_props.mapping_preview:
                box.label(text="No mapping yet. Press 'Convert Rig'.")
            else:
                for item in rig2ue_props.mapping_preview:
                    row = box.row()
                    row.label(text=item.target_bone)
                    row.prop(item, "source_bone", text="")
                    if not item.source_bone:
                        row.alert = True

def register():
    bpy.utils.register_class(Rig2UE_PT_MappingPanel)

def unregister():
    bpy.utils.unregister_class(Rig2UE_PT_MappingPanel)
