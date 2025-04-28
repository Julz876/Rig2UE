import bpy
import math

class Rig2UE_OT_PoseCorrector(bpy.types.Operator):
    bl_idname = "rig2ue.correct_pose"
    bl_label = "Correct Pose (A-Pose ⇆ T-Pose)"
    bl_description = "Adjust arm bones to switch between A-Pose and T-Pose."
    bl_options = {'REGISTER', 'UNDO'}

    direction: bpy.props.EnumProperty(
        name="Direction",
        items=[
            ('APOSE_TO_TPOSE', "A-Pose → T-Pose", ""),
            ('TPOSE_TO_APOSE', "T-Pose → A-Pose", ""),
        ],
        default='APOSE_TO_TPOSE'
    )

    rotation_angle: bpy.props.FloatProperty(
        name="Rotation Angle",
        default=math.radians(20),  # About 20 degrees correction
        description="Angle to rotate the arms upward or downward"
    )

    def execute(self, context):
        rig2ue_props = context.scene.rig2ue_props
        target_rig = bpy.data.objects.get("UE_Target_Rig")
        if not target_rig:
            self.report({'ERROR'}, "Target rig not found.")
            return {'CANCELLED'}
        
        bpy.context.view_layer.objects.active = target_rig
        bpy.ops.object.mode_set(mode='POSE')

         # Bones that need larger rotation
        large_bones = ["clavicle_l", "upperarm_l", "clavicle_r", "upperarm_r"]

        # Bones that need smaller rotation
        small_bones = ["lowerarm_l", "hand_l", "lowerarm_r", "hand_r"]

        for bone_name in large_bones + small_bones:
            if bone_name in target_rig.pose.bones:
                pbone = target_rig.pose.bones[bone_name]
                pbone.rotation_mode = 'XYZ'
                if bone_name in large_bones:
                    if self.direction == 'APOSE_TO_TPOSE':
                        pbone.rotation_euler.x -= self.rotation_angle
                    else:
                        pbone.rotation_euler.x += self.rotation_angle
                else:  # small bones
                    small_angle = self.rotation_angle * 0.5
                    if self.direction == 'APOSE_TO_TPOSE':
                        pbone.rotation_euler.x -= small_angle
                    else:
                        pbone.rotation_euler.x += small_angle

        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Pose correction applied.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(Rig2UE_OT_PoseCorrector)

def unregister():
    bpy.utils.unregister_class(Rig2UE_OT_PoseCorrector)