import bpy


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
    bpy.utils.register_class(WM_OT_myOp)


def unregister():
    bpy.utils.unregister_class(WM_OT_myOp)


if __name__ == "__main__":
    register()
    bpy.ops.wm.myop('INVOKE_DEFAULT') 
