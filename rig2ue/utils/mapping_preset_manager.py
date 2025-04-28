import bpy
import os
import json

def get_presets_folder():
    presets_folder = bpy.path.abspath("//presets/rig2ue_mappings/")
    if not os.path.exists(presets_folder):
        os.makedirs(presets_folder)
    return presets_folder

def save_mapping_preset(rig2ue_props, filename):
    if not bpy.data.is_saved:
        def draw(self, context):
            self.layout.label(text="⚠️ Please save your project before saving presets!")
        bpy.context.window_manager.popup_menu(draw, title="Rig2UE Save Preset Warning", icon='ERROR')
        return None

    data = {}
    for mapping in rig2ue_props.mapping_preview:
        data[mapping.target_bone] = mapping.source_bone

    presets_folder = get_presets_folder()
    full_path = os.path.join(presets_folder, filename)

    with open(full_path, 'w') as f:
        json.dump(data, f, indent=4)

    def draw(self, context):
        self.layout.label(text="Preset saved to:")
        self.layout.label(text=full_path)

    bpy.context.window_manager.popup_menu(draw, title="Rig2UE Save Preset", icon='FILE_TICK')
    return full_path

def load_mapping_preset(rig2ue_props, filename):
    presets_folder = get_presets_folder()
    full_path = os.path.join(presets_folder, filename)

    if not os.path.exists(full_path):
        def draw(self, context):
            self.layout.label(text="⚠️ Preset file not found!")
        bpy.context.window_manager.popup_menu(draw, title="Rig2UE Load Preset Error", icon='ERROR')
        return False

    with open(full_path, 'r') as f:
        data = json.load(f)

    rig2ue_props.mapping_preview.clear()

    for target_bone, source_bone in data.items():
        item = rig2ue_props.mapping_preview.add()
        item.target_bone = target_bone
        item.source_bone = source_bone

    def draw(self, context):
        self.layout.label(text="Preset loaded successfully!")
    bpy.context.window_manager.popup_menu(draw, title="Rig2UE Load Preset", icon='FILE_TICK')

    return True
