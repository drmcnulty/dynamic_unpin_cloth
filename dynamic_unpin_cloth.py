bl_info = {
    "name": "Dynamic Unpin Cloth",
    "description": "Turn a Mesh to Pinned Cloth and Allow Dynamic Paint Brushes to unpin it",
    "author": "David McNulty",
    "version": (1,0),
    "blender": (3, 00, 0),
    "location": "Viewport Object Menu > Dynamic Unpin Cloth",
    "category": "Object",
}

import bpy

# Split Edges. Requires object to already be selected. Returns object to OBJECT mode
def split_edges():
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_split(type='EDGE')
    finally:
        bpy.ops.object.mode_set(mode='OBJECT')
     

def clothify(obj):
    # put all vertices in a group (for later cloth pinning)
    v_groups_pin = obj.vertex_groups.get('pin') \
                   or obj.vertex_groups.new(name='pin')
    v_groups_pin.add([vert.index for vert in obj.data.vertices],
                     1.0,
                     'REPLACE')

    # also put all vertices in a paint group for later dynamic painting
    v_groups_paint = obj.vertex_groups.get('paint') or obj.vertex_groups.new(name='paint')
    v_groups_paint.add([vert.index for vert in obj.data.vertices], 0.0, 'REPLACE')


    # DYNAMIC PAINT
    if not 'DYNAMIC_PAINT' in [m.type for m in obj.modifiers]:
        obj.modifiers.new('Dynamic Paint', 'DYNAMIC_PAINT')
        #bpy.ops.object.modifier_add(type='DYNAMIC_PAINT')
    obj.modifiers["Dynamic Paint"].ui_type = 'CANVAS'
    canvas_settings = obj.modifiers["Dynamic Paint"].canvas_settings
    if not canvas_settings:
        bpy.ops.dpaint.type_toggle(type='CANVAS')
        canvas_settings = obj.modifiers["Dynamic Paint"].canvas_settings
    surfaces = canvas_settings.canvas_surfaces
    if not surfaces:
        #raise Exception(f'No Dynamic Paint canvas surfaces exist on Object "{obj.name}"')
        bpy.ops.dpaint.surface_slot_add()

    # TODO: get existing "destructo_surface" or create new
    surface = surfaces.get('Surface')
    if not surface:
        surface = bpy.ops.dpaint.surface_slot_add()    

    surface.frame_substeps = 5
    surface.surface_type = 'WEIGHT'
    surface.output_name_a = "paint"


    # WEIGHT MIX
    weight_mixer = obj.modifiers.get('Dynamic Cloth Weight Mix') \
                   or obj.modifiers.new('Dynamic Cloth Weight Mix', 'VERTEX_WEIGHT_MIX')
    weight_mixer.vertex_group_a = 'pin'
    weight_mixer.vertex_group_b = 'paint'
    weight_mixer.mix_set = 'A'
    weight_mixer.mix_mode = 'SUB'


    # CLOTH
    if not 'CLOTH' in [m.type for m in obj.modifiers]:
        bpy.ops.object.modifier_add(type='CLOTH')
    obj.modifiers["Cloth"].settings.vertex_group_mass = 'pin'
    obj.modifiers["Cloth"].collision_settings.collision_quality = 3
    obj.modifiers["Cloth"].collision_settings.distance_min = 0.002



class DynamicUnpinCloth(bpy.types.Operator):
    """Turn a Mesh to Pinned Cloth and Allow Dynamic Paint Brushes to unpin it"""
    bl_idname = "object.dynamic_unpin_cloth"
    bl_label = "Dynamic Unpin Cloth"
    bl_options = {'REGISTER', 'UNDO'}
    
    shatter: bpy.props.BoolProperty(
        name="Shatter", 
        description="Split Along all Edges to create a shattering effect",
        default=False)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                if self.shatter:
                    split_edges()
                clothify(obj)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(DynamicUnpinCloth.bl_idname, text=DynamicUnpinCloth.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Dynamic Unpin Cloth" for quick access).
def register():
    bpy.utils.register_class(DynamicUnpinCloth)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(DynamicUnpinCloth)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.dynamic_unpin_cloth()


