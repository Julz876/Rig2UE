import bpy

def get_armature_list(self, context):
    armature_items = []
    for obj in context.scene.objects:
        if obj.type == 'ARMATURE':
            armature_items.append((obj.name, obj.name, ""))
    if not armature_items:
        armature_items.append(('None', 'No Armatures Found', ""))
    return armature_items


class Rig2UE_OT_ResetExportDefaults(bpy.types.Operator):
    bl_idname = "rig2ue.reset_export_defaults"
    bl_label = "Reset Export Settings to Defaults"

    def execute(self, context):
        prefs = bpy.context.preferences.addons[__package__].preferences
        rig2ue_props = bpy.context.scene.rig2ue_props

        rig2ue_props.export_folder = prefs.default_export_folder
        rig2ue_props.export_filename = prefs.default_export_filename

        self.report({'INFO'}, "Export settings reset to defaults.")
        return {'FINISHED'}


class Rig2UE_PT_MainPanel(bpy.types.Panel):
    bl_label = "Rig2UE Tools"
    bl_idname = "RIG2UE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rig2UE'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rig2ue_props = scene.rig2ue_props

        # Lazy apply defaults if blank
        if not rig2ue_props.export_folder or not rig2ue_props.export_filename:
            prefs = bpy.context.preferences.addons[__package__].preferences
            if not rig2ue_props.export_folder:
                rig2ue_props.export_folder = prefs.default_export_folder
            if not rig2ue_props.export_filename:
                rig2ue_props.export_filename = prefs.default_export_filename

        layout.prop(rig2ue_props, "enable_advanced_mode", toggle=True)

        layout.label(text="Select Source Rig:")
        layout.prop(rig2ue_props, "source_armature", text="")

        layout.label(text="Select Target Profile:")
        layout.prop(rig2ue_props, "target_profile", text="")

        layout.separator()
        row = layout.row(align=True)
        row.operator("rig2ue.convert_rig", text="Convert Rig", icon='ARMATURE_DATA')
        row.operator("rig2ue.refresh_mapping", text="", icon='FILE_REFRESH')

        layout.separator()
        layout.label(text="Pose Correction:")
        row = layout.row(align=True)
        row.operator("rig2ue.correct_pose", text="A-Pose → T-Pose").direction = 'APOSE_TO_TPOSE'
        row.operator("rig2ue.correct_pose", text="T-Pose → A-Pose").direction = 'TPOSE_TO_APOSE'


def register():
    bpy.utils.register_class(Rig2UE_PT_MainPanel)
    bpy.utils.register_class(Rig2UE_OT_ResetExportDefaults)

def unregister():
    bpy.utils.unregister_class(Rig2UE_PT_MainPanel)
    bpy.utils.unregister_class(Rig2UE_OT_ResetExportDefaults)
