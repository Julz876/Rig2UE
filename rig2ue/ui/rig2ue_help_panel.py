import bpy

class Rig2UE_PT_HelpPanel(bpy.types.Panel):
    bl_label = "Rig2UE Help/About"
    bl_idname = "RIG2UE_PT_help_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rig2UE'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Rig2UE v1.0", icon='INFO')
        layout.label(text="Quick Guide:")

        layout.box().label(text="1. Select your source rig.")
        layout.box().label(text="2. Choose UE5, UE4, or MetaHuman profile.")
        layout.box().label(text="3. Press [Convert Rig].")
        layout.box().label(text="4. (Optional) Correct Pose A⇆T.")
        layout.box().label(text="5. Export clean FBX for Unreal.")

        layout.separator()
        layout.label(text="Useful Tips:")
        layout.box().label(text="- Use Save/Load Presets for multiple rigs.")
        layout.box().label(text="- Adjust bone mapping if needed manually.")
        layout.box().label(text="- Always check IK bones placement.")
        layout.box().label(text="- FBX export is fully Unreal-ready!")

        layout.separator()
        layout.label(text="Credits:")
        layout.box().label(text="Created by: KingxJulz")
        layout.box().label(text="Blender 4.2+ Compatible.")
        layout.box().label(text="For Unreal Engine 5 retargeting.")
        
def register():
    bpy.utils.register_class(Rig2UE_PT_HelpPanel)

def unregister():
    bpy.utils.unregister_class(Rig2UE_PT_HelpPanel)
