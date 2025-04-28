import bpy
import os

class Rig2UE_OT_ExportFBX(bpy.types.Operator):
    bl_idname = "rig2ue.export_fbx"
    bl_label = "Export to FBX for UE5"
    bl_description = "Export the UE Target Rig to a clean FBX file ready for Unreal Engine."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        rig2ue_props = scene.rig2ue_props

        target_rig = bpy.data.objects.get("UE_Target_Rig")
        if not target_rig:
            self.report({'ERROR'}, "UE_Target_Rig not found. Please convert rig first.")
            return {'CANCELLED'}

        export_folder = bpy.path.abspath(rig2ue_props.export_folder)
        export_name = rig2ue_props.export_filename or "exported_rig"
        export_path = os.path.join(export_folder, f"{export_name}.fbx")

        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        # Deselect everything
        bpy.ops.object.select_all(action='DESELECT')

        # Select only the target rig + meshes skinned to it
        target_rig.select_set(True)
        for obj in scene.objects:
            if obj.type == 'MESH':
                for mod in obj.modifiers:
                    if mod.type == 'ARMATURE' and mod.object == target_rig:
                        obj.select_set(True)

        bpy.context.view_layer.objects.active = target_rig

        bpy.ops.export_scene.fbx(
            filepath=export_path,
            use_selection=True,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            global_scale=1.0,
            axis_forward='-Z',
            axis_up='Y',
            object_types={'ARMATURE', 'MESH'},
            bake_anim=True,
            add_leaf_bones=False,
            primary_bone_axis='Y',
            secondary_bone_axis='X',
            use_armature_deform_only=True
        )

        self.report({'INFO'}, f"Exported FBX to {export_path}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(Rig2UE_OT_ExportFBX)

def unregister():
    bpy.utils.unregister_class(Rig2UE_OT_ExportFBX)
