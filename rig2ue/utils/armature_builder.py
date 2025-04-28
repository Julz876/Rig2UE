import bpy
import mathutils

def build_target_armature(context, rig2ue_props):
    source_rig_name = rig2ue_props.source_armature
    source_rig = bpy.data.objects.get(source_rig_name)
    if not source_rig:
        print("[Rig2UE] Source rig not found.")
        return None

    armature_data = bpy.data.armatures.new(name="UE_Target_Rig")
    target_rig = bpy.data.objects.new("UE_Target_Rig", armature_data)
    context.collection.objects.link(target_rig)

    bpy.context.view_layer.objects.active = target_rig
    bpy.ops.object.mode_set(mode='EDIT')

    edit_bones = target_rig.data.edit_bones
    source_bones = source_rig.data.bones
    bone_lookup = {b.name: b for b in source_bones}

    for mapping in rig2ue_props.mapping_preview:
        target_bone_name = mapping.target_bone
        source_bone_name = mapping.source_bone

        new_bone = edit_bones.new(target_bone_name)

        if source_bone_name and source_bone_name in bone_lookup:
            src_bone = bone_lookup[source_bone_name]
            new_bone.head = src_bone.head_local
            new_bone.tail = src_bone.tail_local
        else:
            related_bone_name = get_related_bone_guess(target_bone_name)
            if related_bone_name and related_bone_name in bone_lookup:
                src_bone = bone_lookup[related_bone_name]
                new_bone.head = src_bone.head_local
                new_bone.tail = (
                    src_bone.head_local[0],
                    src_bone.head_local[1] + 0.2,
                    src_bone.head_local[2]
                )
            else:
                new_bone.head = (0.0, 0.0, 0.0)
                new_bone.tail = (0.0, 0.1, 0.0)

        # Fix arm roll specifically
        if any(key in target_bone_name.lower() for key in ["clavicle", "upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky" ]):
            new_bone.align_roll(mathutils.Vector((0, 1, 0)))

    apply_full_ue5_parenting(edit_bones)

    bpy.ops.object.mode_set(mode='OBJECT')
    print("[Rig2UE] Target rig created successfully!")
    return target_rig


def get_related_bone_guess(target_bone_name):
    # Guess related source bone for missing IK/FK bones
    if "hand_ik_l" in target_bone_name:
        return "hand_l"
    elif "hand_ik_r" in target_bone_name:
        return "hand_r"
    elif "foot_ik_l" in target_bone_name:
        return "foot_l"
    elif "foot_ik_r" in target_bone_name:
        return "foot_r"
    elif "spine_ik" in target_bone_name:
        return "spine_01"
    return None

def apply_full_ue5_parenting(edit_bones):
    parenting_rules = {
        "pelvis": "root",
        "spine_01": "pelvis",
        "spine_02": "spine_01",
        "spine_03": "spine_02",
        "neck_01": "spine_03",
        "neck_02": "neck_01",
        "head": "neck_02",

        "clavicle_pec_l": "spine_03",
        "clavicle_l": "spine_03",
        "upperarm_l": "clavicle_l",
        "lowerarm_l": "upperarm_l",
        "hand_l": "lowerarm_l",

        "thumb_01_l": "hand_l",
        "thumb_02_l": "thumb_01_l",
        "thumb_03_l": "thumb_02_l",

        "index_metacarpal_l": "hand_l",
        "index_01_l": "index_metacarpal_l",
        "index_02_l": "index_01_l",
        "index_03_l": "index_02_l",

        "middle_metacarpal_l": "hand_l",
        "middle_01_l": "middle_metacarpal_l",
        "middle_02_l": "middle_01_l",
        "middle_03_l": "middle_02_l",

        "ring_metacarpal_l": "hand_l",
        "ring_01_l": "ring_metacarpal_l",
        "ring_02_l": "ring_01_l",
        "ring_03_l": "ring_02_l",

        "pinky_metacarpal_l": "hand_l",
        "pinky_01_l": "pinky_metacarpal_l",
        "pinky_02_l": "pinky_01_l",
        "pinky_03_l": "pinky_02_l",

        "clavicle_pec_r": "spine_03",
        "clavicle_r": "spine_03",
        "upperarm_r": "clavicle_r",
        "lowerarm_r": "upperarm_r",
        "hand_r": "lowerarm_r",

        "thumb_01_r": "hand_r",
        "thumb_02_r": "thumb_01_r",
        "thumb_03_r": "thumb_02_r",

        "index_metacarpal_r": "hand_r",
        "index_01_r": "index_metacarpal_r",
        "index_02_r": "index_01_l",
        "index_03_r": "index_02_r",

        "middle_metacarpal_r": "hand_r",
        "middle_01_r": "middle_metacarpal_r",
        "middle_02_r": "middle_01_r",
        "middle_03_r": "middle_02_r",

        "ring_metacarpal_r": "hand_r",
        "ring_01_r": "ring_metacarpal_r",
        "ring_02_r": "ring_01_r",
        "ring_03_r": "ring_02_r",

        "pinky_metacarpal_r": "hand_r",
        "pinky_01_r": "pinky_metacarpal_r",
        "pinky_02_r": "pinky_01_r",
        "pinky_03_r": "pinky_02_r",
        
        "thigh_l": "pelvis",
        "calf_l": "thigh_l",
        "foot_l": "calf_l",
        "ball_l": "foot_l",
        "ankle_bck_l": "calf_l",

        "thigh_r": "pelvis",
        "calf_r": "thigh_r",
        "foot_r": "calf_r",
        "ball_r": "foot_r",
        "ankle_bck_r": "calf_r",

        "hand_ik_l": "root",
        "hand_ik_r": "root",
        "foot_ik_l": "root",
        "foot_ik_r": "root",
        "spine_ik": "root",
    }

    for child_name, parent_name in parenting_rules.items():
        if child_name in edit_bones and parent_name in edit_bones:
            edit_bones[child_name].parent = edit_bones[parent_name]
