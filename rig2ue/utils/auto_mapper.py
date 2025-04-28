import difflib

def map_bones(source_armature, target_profile):
    """
    Automatically map bones from the source rig to the target profile.
    
    :param source_armature: Blender Armature Object (source rig)
    :param target_profile: Dict of target skeleton bone names
    :return: Dictionary of source_bone_name -> target_bone_name mappings
    """

    source_bones = [bone.name for bone in source_armature.data.bones]
    target_bones = list(target_profile.keys())

    bone_mapping = {}

    for target_bone in target_bones:
        match = find_best_match(target_bone, source_bones)
        if match:
            bone_mapping[target_bone] = match
        else:
            bone_mapping[target_bone] = None  # No good match found

    return bone_mapping

def find_best_match(target_bone, source_bone_list):
    """
    Find the best matching source bone name for a given target bone name.
    """
    if not source_bone_list:
        return None
    
    # Use difflib to find close matches
    matches = difflib.get_close_matches(target_bone, source_bone_list, n=1, cutoff=0.4)
    if matches:
        return matches[0]
    
    # Try looser match manually
    for src_bone in source_bone_list:
        if target_bone.lower() in src_bone.lower() or src_bone.lower() in target_bone.lower():
            return src_bone

    return None
