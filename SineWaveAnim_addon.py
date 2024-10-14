bl_info = {
    "name": "Infinite Sine Wave Animation Addon",
    "blender": (3, 6, 0),
    "category": "Animation",
    "author": "Amir",
}

import bpy
import math

class InfiniteSineWaveOperator(bpy.types.Operator):
    """Animate selected object in an infinite sine wave motion"""
    bl_idname = "object.infinite_sine_wave"
    bl_label = "Create Infinite Sine Wave Animation"
    
    amplitude: bpy.props.FloatProperty(name="Amplitude", default=1.0, min=0.0)
    frequency: bpy.props.FloatProperty(name="Frequency", default=1.0, min=0.0)
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object.")
            return {'CANCELLED'}
        
        # Clear existing keyframes
        obj.animation_data_clear()
        
        # Get the end frame from scene properties
        frame_end = context.scene.sine_wave_frame_end

        # Create sine wave animation from frame 1 to frame_end
        for frame in range(1, frame_end + 1):
            # Calculate sine wave value
            z_value = self.amplitude * math.sin((frame / 20.0) * self.frequency)
            obj.location.z = z_value
            
            # Insert keyframe for Z location
            obj.keyframe_insert(data_path="location", frame=frame)

        # Set the end frame for the scene to the specified value
        context.scene.frame_end = frame_end
        
        return {'FINISHED'}


class InfiniteSineWavePanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport sidebar"""
    bl_label = "Infinite Sine Wave Animation"
    bl_idname = "VIEW3D_PT_infinite_sine_wave"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sine Wave"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            layout.label(text="Select a mesh object.")
            return

        # Amplitude property
        row = layout.row()
        row.prop(context.scene, "sine_wave_amplitude", text="Amplitude")
        
        # Frequency property
        row = layout.row()
        row.prop(context.scene, "sine_wave_frequency", text="Frequency")
        
        # End Frame property
        row = layout.row()
        row.prop(context.scene, "sine_wave_frame_end", text="End Frame")

        # Operator button
        layout.operator(InfiniteSineWaveOperator.bl_idname, text="Create Infinite Sine Wave")


def register():
    bpy.utils.register_class(InfiniteSineWaveOperator)
    bpy.utils.register_class(InfiniteSineWavePanel)
    
    # Add properties to the scene
    bpy.types.Scene.sine_wave_amplitude = bpy.props.FloatProperty(name="Amplitude", default=1.0, min=0.0)
    bpy.types.Scene.sine_wave_frequency = bpy.props.FloatProperty(name="Frequency", default=1.0, min=0.0)
    bpy.types.Scene.sine_wave_frame_end = bpy.props.IntProperty(name="End Frame", default=250, min=1)


def unregister():
    bpy.utils.unregister_class(InfiniteSineWavePanel)
    bpy.utils.unregister_class(InfiniteSineWaveOperator)

    # Remove properties
    del bpy.types.Scene.sine_wave_amplitude
    del bpy.types.Scene.sine_wave_frequency
    del bpy.types.Scene.sine_wave_frame_end


if __name__ == "__main__":
    register()
