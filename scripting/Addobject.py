bl_info = {
    "name": "Object Adder",
    "author": "Surya",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Tool",
    "category": "Add Mesh",
}

import bpy

class TestPanel(bpy.types.Panel):
    bl_label = "Test Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My Tools"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Add an object", icon='CUBE')

        col = layout.column()
        col.operator("wm.myop", text="Add Cube", icon='MESH_CUBE')  
        col.operator("mesh.primitive_uv_sphere_add", text="Add UV Sphere", icon='MESH_UVSPHERE')
        col.operator("object.text_add", text="Add Text", icon='OUTLINER_OB_FONT')

        layout.separator()
        layout.label(text="Utilities", icon='TOOL_SETTINGS')
        col.operator("object.delete", text="Delete Selected", icon='TRASH')


class Scale(bpy.types.Panel):
    bl_label = "Scaling"
    bl_idname = "PT_Scale"  
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My Tools"
    bl_parent_id = "PT_TestPanel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select an option to scale an object.", icon='FONT_DATA')

        obj = context.object
        col = layout.column()

        if obj:
            col.prop(obj, "scale") 
        else:
            layout.label(text="No object selected", icon='ERROR')


class PanelA(bpy.types.Panel):
    bl_label = "Panel A"
    bl_idname = "PT_PanelA"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My Tools"
    bl_parent_id = "PT_TestPanel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is Panel A", icon='FONT_DATA')
        col = layout.column()
        col.operator("object.text_add", text="Add Text object", icon='FONT_DATA')


class Modifier(bpy.types.Panel):
    bl_label = "Modifier"
    bl_idname = "PT_PanelB"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My Tools"
    bl_parent_id = "PT_TestPanel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Apply Modifiers", icon='MODIFIER')

        col = layout.column()
        col.operator("object.modifier_add", text="Add Subdivision", icon='MOD_SUBSURF').type = 'SUBSURF'
        col.operator("object.modifier_add", text="Add Bevel", icon='MOD_BEVEL').type = 'BEVEL'
        col.operator("object.modifier_add", text="Add Solidify", icon='MOD_SOLIDIFY').type = 'SOLIDIFY'
        col.operator("object.modifier_add", text="Add Mirror", icon='MOD_MIRROR').type = 'MIRROR'
        col.operator("object.modifier_add", text="Add Array", icon='MOD_ARRAY').type = 'ARRAY'


class Special(bpy.types.Panel):
    bl_label = "Special"
    bl_idname = "PT_Special"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My Tools"
    bl_parent_id = "PT_TestPanel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select a special option", icon='MOD_SMOOTH')

        col = layout.column()
        col.operator("object.shade_smooth", text="Smooth Shading", icon='SHADING_RENDERED')
        col.operator("object.modifier_add", text="Add Subdivision", icon='MOD_SUBSURF').type = 'SUBSURF'
        
        
class WM_OT_myOp(bpy.types.Operator):
    bl_label = "Add Cube Dialogue Box"
    bl_idname = "wm.myop"

    text: bpy.props.StringProperty(name="Enter Object Name", default="MyCube")
    scale: bpy.props.FloatVectorProperty(name="Scale", default=(1, 1, 1), size=3)

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        obj = context.object
        obj.name = self.text  
        obj.scale = self.scale  

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(Scale)
    bpy.utils.register_class(PanelA)
    bpy.utils.register_class(Modifier)
    bpy.utils.register_class(Special)
    bpy.utils.register_class(WM_OT_myOp)

def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(Scale)
    bpy.utils.unregister_class(PanelA)
    bpy.utils.unregister_class(Modifier)
    bpy.utils.unregister_class(Special)
    bpy.utils.unregister_class(WM_OT_myOp)

if __name__ == "__main__":
    register()
