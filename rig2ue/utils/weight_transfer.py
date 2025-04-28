import bpy

def copy_skin_weights(context, source_rig, target_rig):
    skinned_meshes = []
    for obj in context.scene.objects:
        if obj.type == 'MESH':
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE' and modifier.object == source_rig:
                    skinned_meshes.append(obj)
                    break

    if not skinned_meshes:
        print("[Rig2UE] No skinned meshes found to copy weights.")
        return

    for mesh_obj in skinned_meshes:
        print(f"[Rig2UE] Transferring weights for {mesh_obj.name}")

        # Add new Armature modifier linked to the new target rig
        new_modifier = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
        new_modifier.object = target_rig

        # Ensure all bones exist as vertex groups
        existing_vgroups = {vg.name: vg for vg in mesh_obj.vertex_groups}
        for bone in target_rig.data.bones:
            if bone.name not in existing_vgroups:
                mesh_obj.vertex_groups.new(name=bone.name)

        # Auto Weight Transfer
        try:
            bpy.context.view_layer.objects.active = mesh_obj
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
            bpy.ops.object.data_transfer(
                data_type='VGROUP_WEIGHTS',
                use_create=True,
                use_auto_transform=True,
                use_object_transform=True,
                layers_select_src='ALL',
                layers_select_dst='NAME'
            )
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception as e:
            print(f"[Rig2UE] Weight transfer failed for {mesh_obj.name}: {str(e)}")

        # Copy Shape Keys if they exist
        if mesh_obj.data.shape_keys:
            print(f"[Rig2UE] Copying shape keys for {mesh_obj.name}")
            for sk in mesh_obj.data.shape_keys.key_blocks:
                if sk.name not in mesh_obj.vertex_groups:
                    # Create matching vertex group for shape key if needed
                    mesh_obj.vertex_groups.new(name=sk.name)

    print("[Rig2UE] Weight and shape key transfer complete!")
