bl_info = {
    "name": "Shader Library",
    "author": "surya",
    "version": (1, 1),
    "blender": (4, 2),
    "location": "View3D > ToolShelf",
    "description": "Adds a New Shader to your Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Shader",
}

import bpy

class ShaderMainPanel(bpy.types.Panel):
    bl_label = "Shader Library"
    bl_idname = "SHADER_PT_MAINPANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shader Library"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Select a Shader:")
        
        layout.operator("shader.diamond_operator", text="Diamond Shader")
        layout.operator("shader.gold_operator", text="Gold Shader")
        layout.operator("shader.silver_operator", text="Silver Shader")
        layout.operator("shader.copper_operator", text="Copper Shader")
        layout.operator("shader.ghost_operator", text="Ghost Shader")
        layout.operator("shader.hologram_operator", text="Hologram Shader")


def assign_material(material):
    """Assigns the created material to the active object."""
    obj = bpy.context.object
    if obj and obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)


class SHADER_OT_DIAMOND(bpy.types.Operator):
    """Creates a Diamond Shader"""
    bl_label = "Diamond Shader"
    bl_idname = "shader.diamond_operator"

    def execute(self, context):
        material = bpy.data.materials.new(name="Diamond")
        material.use_nodes = True

        # Remove default Principled BSDF
        material.node_tree.nodes.remove(material.node_tree.nodes.get('Principled BSDF'))

        # Create Glass Shader Nodes for RGB reflections
        glass_colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 1, 1)]
        glass_nodes = []
        
        for i, color in enumerate(glass_colors):
            glass_node = material.node_tree.nodes.new('ShaderNodeBsdfGlass')
            glass_node.inputs[0].default_value = color
            glass_node.inputs[2].default_value = 2.42  # Diamond IOR
            glass_nodes.append(glass_node)
        
        # Add Shader Nodes to combine glass effects
        add1 = material.node_tree.nodes.new('ShaderNodeAddShader')
        add2 = material.node_tree.nodes.new('ShaderNodeAddShader')
        mix = material.node_tree.nodes.new('ShaderNodeMixShader')

        # Connect Nodes
        material.node_tree.links.new(glass_nodes[0].outputs[0], add1.inputs[0])
        material.node_tree.links.new(glass_nodes[1].outputs[0], add1.inputs[1])
        material.node_tree.links.new(add1.outputs[0], add2.inputs[0])
        material.node_tree.links.new(glass_nodes[2].outputs[0], add2.inputs[1])
        material.node_tree.links.new(add2.outputs[0], mix.inputs[1])
        material.node_tree.links.new(glass_nodes[3].outputs[0], mix.inputs[2])

        # Output
        material_output = material.node_tree.nodes.get('Material Output')
        material.node_tree.links.new(mix.outputs[0], material_output.inputs['Surface'])

        assign_material(material)
        return {'FINISHED'}


class SHADER_OT_GOLD(bpy.types.Operator):
    """Creates a Gold Shader"""
    bl_label = "Gold Shader"
    bl_idname = "shader.gold_operator"

    def execute(self, context):
        material = bpy.data.materials.new(name="Gold")
        material.use_nodes = True
        
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = (1.0, 0.85, 0.2, 1)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.2

        assign_material(material)
        return {'FINISHED'}


class SHADER_OT_SILVER(bpy.types.Operator):
    """Creates a Silver Shader"""
    bl_label = "Silver Shader"
    bl_idname = "shader.silver_operator"

    def execute(self, context):
        material = bpy.data.materials.new(name="Silver")
        material.use_nodes = True
        
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.1

        assign_material(material)
        return {'FINISHED'}


class SHADER_OT_COPPER(bpy.types.Operator):
    """Creates a Copper Shader"""
    bl_label = "Copper Shader"
    bl_idname = "shader.copper_operator"

    def execute(self, context):
        material = bpy.data.materials.new(name="Copper")
        material.use_nodes = True
        
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = (0.8, 0.4, 0.2, 1)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.3

        assign_material(material)
        return {'FINISHED'}


class SHADER_OT_GHOST(bpy.types.Operator):
    """Creates a Ghost Shader"""
    bl_label = "Ghost Shader"
    bl_idname = "shader.ghost_operator"

    def execute(self, context):
        material = bpy.data.materials.new(name="Ghost")
        material.use_nodes = True
        
        mix_shader = material.node_tree.nodes.new('ShaderNodeMixShader')
        transparent = material.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        glass = material.node_tree.nodes.new('ShaderNodeBsdfGlass')

        glass.inputs[0].default_value = (0.8, 0.9, 1.0, 1)  # Light blue tint
        glass.inputs[2].default_value = 1.1  # Low IOR for ethereal effect

        material.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[1])
        material.node_tree.links.new(glass.outputs[0], mix_shader.inputs[2])
        material.node_tree.links.new(mix_shader.outputs[0], material.node_tree.nodes.get('Material Output').inputs['Surface'])

        assign_material(material)
        return {'FINISHED'}


class SHADER_OT_HOLOGRAM(bpy.types.Operator):
    """Creates a Hologram Shader"""
    bl_label = "Hologram Shader"
    bl_idname = "shader.hologram_operator"

    def execute(self, context):
        material = bpy.data.materials.new(name="Hologram")
        material.use_nodes = True
        
        emission = material.node_tree.nodes.new('ShaderNodeEmission')
        emission.inputs[0].default_value = (0.0, 1.0, 1.0, 1)  # Cyan glow
        emission.inputs[1].default_value = 2.0

        material.node_tree.links.new(emission.outputs[0], material.node_tree.nodes.get('Material Output').inputs['Surface'])

        assign_material(material)
        return {'FINISHED'}


def register():
    for cls in [ShaderMainPanel, SHADER_OT_DIAMOND, SHADER_OT_GOLD, SHADER_OT_SILVER, SHADER_OT_COPPER, SHADER_OT_GHOST, SHADER_OT_HOLOGRAM]:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed([ShaderMainPanel, SHADER_OT_DIAMOND, SHADER_OT_GOLD, SHADER_OT_SILVER, SHADER_OT_COPPER, SHADER_OT_GHOST, SHADER_OT_HOLOGRAM]):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
