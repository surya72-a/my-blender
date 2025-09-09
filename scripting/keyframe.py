import bpy


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "New"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("shader.neon_operator")


class SHADER_OT_NEON(bpy.types.Operator):
    """Operator to add a neon shader"""
    bl_label = "Add Neon Shader"
    bl_idname = "shader.neon_operator"

    def execute(self, context):
        cur_frame = bpy.context.scene.frame_current

        obj = context.object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object first!")
            return {'CANCELLED'}

        # Create or get material
        material_name = "NeonMaterial"
        material = bpy.data.materials.get(material_name) or bpy.data.materials.new(name=material_name)
        material.use_nodes = True

        tree = material.node_tree

        nodes = tree.nodes
        links = tree.links

        # Remove existing nodes
        for node in nodes:
            nodes.remove(node)

        # Add an emission shader
        emission = nodes.new(type='ShaderNodeEmission')
        emission.location = (0, 300)
        emission.inputs[0].default_value = (0.3, 0.7, 1, 1)  # Light blue color
        emission.inputs[1].default_value = 15  # Strength
        emission.inputs[1].keyframe_insert("default_value", frame=cur_frame)

        # Add material output
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 300)

        # Link nodes
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        # Assign material to object
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

        # Enable bloom effect in Eevee
        scene = bpy.context.scene
        if scene.render.engine == 'BLENDER_EEVEE':
            scene.eevee.use_bloom = True

        # Switch to Rendered View
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'

        # ✅ Add Noise Modifier to Emission Strength
        if tree.animation_data and tree.animation_data.action:
            data_path = f'nodes["{emission.name}"].inputs[1].default_value'
            fcurves = tree.animation_data.action.fcurves
            fc = fcurves.find(data_path)

            if fc:
                new_mod = fc.modifiers.new('NOISE')
                new_mod.strength = 2
                new_mod.depth = 1

        return {'FINISHED'}


def register():
    bpy.utils.register_class(HelloWorldPanel)
    bpy.utils.register_class(SHADER_OT_NEON)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(SHADER_OT_NEON)


if __name__ == "__main__":
    register()
