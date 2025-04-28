import bpy

class Rig2UE_OT_MappingEditor(bpy.types.Operator):
    bl_idname = "rig2ue.mapping_editor"
    bl_label = "Bone Mapping Editor"
    bl_description = "Edit bone mapping manually inside a popup window."

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rig2ue_props = scene.rig2ue_props

        box = layout.box()
        for item in rig2ue_props.mapping_preview:
            row = box.row()
            row.label(text=item.target_bone)
            row.prop(item, "source_bone", text="")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

def register():
    bpy.utils.register_class(Rig2UE_OT_MappingEditor)

def unregister():
    bpy.utils.unregister_class(Rig2UE_OT_MappingEditor)
