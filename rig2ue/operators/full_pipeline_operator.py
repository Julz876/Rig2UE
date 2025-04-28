import bpy
import os
from ..utils import armature_builder, weight_transfer
from ..utils import auto_mapper
from ..utils import bone_mapping_profiles

class Rig2UE_OT_FullPipeline(bpy.types.Operator):
    bl_idname = "rig2ue.full_pipeline"
    bl_label = "One-Click Full Export"
    bl_description = "Convert Rig + Copy Skin Weights + Export FBX in one click!"
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
            self.report({'ERROR'}, "Selected rig not found.")
            return {'CANCELLED'}

        profile = bone_mapping_profiles.PROFILES.get(target_profile_key)
        if not profile:
            self.report({'ERROR'}, "Target profile not found.")
            return {'CANCELLED'}
        
        def show_popup(self, message, title="Success", icon='CHECKMARK'):
            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

        # Step 1: Auto Bone Mapping
        bone_map = auto_mapper.map_bones(source_rig, profile)

        # Update mapping preview
        rig2ue_props.mapping_preview.clear()
        for target_bone, source_bone in bone_map.items():
            item = rig2ue_props.mapping_preview.add()
            item.target_bone = target_bone
            item.source_bone = source_bone if source_bone else ""

        # Step 2: Build Target Rig
        target_rig = armature_builder.build_target_armature(context, rig2ue_props)
        if not target_rig:
            self.report({'ERROR'}, "Failed to create Target Rig.")
            return {'CANCELLED'}

        # Step 3: Copy Skin Weights and blend shapes if available
        weight_transfer.copy_skin_weights(context, source_rig, target_rig)

        # Step 4: Export FBX
        export_folder = bpy.path.abspath(rig2ue_props.export_folder)
        export_name = rig2ue_props.export_filename or "exported_rig"
        export_path = os.path.join(export_folder, f"{export_name}.fbx")

        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        bpy.ops.object.select_all(action='DESELECT')

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
        self.report({'INFO'}, f"Full pipeline complete! Exported FBX to {export_path}")

        self.show_popup("Full Export Complete! FBX Ready.", "Rig2UE Export", 'EXPORT')

        return {'FINISHED'}

def register():
    bpy.utils.register_class(Rig2UE_OT_FullPipeline)

def unregister():
    bpy.utils.unregister_class(Rig2UE_OT_FullPipeline)
