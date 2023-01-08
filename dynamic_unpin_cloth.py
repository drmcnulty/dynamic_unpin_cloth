bl_info = {
    "name": "Dynamic Unpin Cloth",
    "description": "Turn a Mesh to Pinned Cloth and Allow Dynamic Paint Brushes to unpin it",
    "author": "David McNulty",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Viewport Object Menu > Dynamic Unpin Cloth",
    "doc_url": "https://github.com/drmcnulty/dynamic_unpin_cloth/blob/main/README.md",
    "tracker_url": "https://github.com/drmcnulty/dynamic_unpin_cloth/issues",
    "category": "Object",
}


import bpy


# TODO overall: eliminate or isolate context-dependent ".ops" calls


def split_edges_op():
    """Split Edges. Requires object to already be selected. Returns object to OBJECT mode"""
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_split(type='EDGE')
    finally:
        bpy.ops.object.mode_set(mode='OBJECT')


def apply_weld(obj):
    if not obj.modifiers.get("Weld Split Edges"):
        obj.modifiers.new("Weld Split Edges", 'WELD')


def configure_vertex_groups(obj):
    """put all vertices in a pinning group and painting group"""
    # put all vertices in a pinning group to control cloth adhesion
    v_groups_pin = obj.vertex_groups.get("pin") or obj.vertex_groups.new(name="pin")
    v_groups_pin.add([vert.index for vert in obj.data.vertices],
                     1.0,
                     'REPLACE')

    # put all vertices in a paint group for later dynamic painting
    v_groups_paint = obj.vertex_groups.get("paint") or obj.vertex_groups.new(name="paint")
    v_groups_paint.add([vert.index for vert in obj.data.vertices], 0.0, 'REPLACE')


def configure_dynamic_paint(obj):
    """Adds a canvas surface to the object that controls the paint vertex group"""
    if 'DYNAMIC_PAINT' not in [m.type for m in obj.modifiers]:
        obj.modifiers.new("Dynamic Paint", 'DYNAMIC_PAINT')
    obj.modifiers["Dynamic Paint"].ui_type = 'CANVAS'

    canvas_settings = obj.modifiers["Dynamic Paint"].canvas_settings
    if not canvas_settings:
        bpy.ops.dpaint.type_toggle(type='CANVAS')
        canvas_settings = obj.modifiers["Dynamic Paint"].canvas_settings

    # TODO: I don't want to overwrite pre-existing surfaces, so get "dynamic_unpin" surface or create new.
    surfaces = canvas_settings.canvas_surfaces
    if not surfaces:
        # raise Exception(f'No Dynamic Paint canvas surfaces exist on Object "{obj.name}"')
        bpy.ops.dpaint.surface_slot_add()

    surface = surfaces.get("Surface")
    if not surface:
        surface = bpy.ops.dpaint.surface_slot_add()

    surface.frame_substeps = 5
    surface.surface_type = 'WEIGHT'
    surface.output_name_a = "paint"


def configure_weight_mix(obj):
    # WEIGHT MIX
    weight_mixer = obj.modifiers.get("Dynamic Cloth Weight Mix") \
                   or obj.modifiers.new("Dynamic Cloth Weight Mix", 'VERTEX_WEIGHT_MIX')
    weight_mixer.vertex_group_a = "pin"
    weight_mixer.vertex_group_b = "paint"
    weight_mixer.mix_set = 'A'
    weight_mixer.mix_mode = 'SUB'


def configure_cloth(obj):
    # CLOTH
    if 'CLOTH' not in [m.type for m in obj.modifiers]:
        bpy.ops.object.modifier_add(type='CLOTH')
    obj.modifiers["Cloth"].settings.vertex_group_mass = "pin"
    obj.modifiers["Cloth"].collision_settings.collision_quality = 3
    obj.modifiers["Cloth"].collision_settings.distance_min = 0.002


def make_cloth_dynamic(obj):
    configure_vertex_groups(obj)
    configure_dynamic_paint(obj)
    configure_weight_mix(obj)
    configure_cloth(obj)


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
                    split_edges_op()
                    make_cloth_dynamic(obj)
                    apply_weld(obj)
                else:
                    make_cloth_dynamic(obj)

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
