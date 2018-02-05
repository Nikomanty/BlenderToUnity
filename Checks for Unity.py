import bpy
import time
import os
from bpy_extras.image_utils import load_image

#Info in User Preference add-ons
bl_info = {
    "name": "Checks for Unity",
    "author": "Niko Mänty",
    "version": (1, 0),
    "blender": (2,78,0),
    "location": "3D View > Tool Self > Misc",
    "category": "Object"}
    
#Apply and rotate to -90 degree by X, Apply that and rotate 90 degree by X
class RotScaleMatTexFix(bpy.types.Operator):
    bl_label = "RotScale Check"
    bl_idname = "object.rot_scale_check"
    bl_options = {'REGISTER', 'UNDO'}
    
    def applyRotScaleDelMatTex(self):
        #Apply current Scale
        bpy.ops.object.transform_apply(scale = True)
        
        #Apply current Rotation and Rotate -90 degrees by X axis
        bpy.ops.object.transform_apply(rotation = True) 
        bpy.ops.transform.rotate(value = -1.5708, axis = (1, 0, 0), constraint_axis = (True, False, False), constraint_orientation = 'GLOBAL')
        
        #Apply current Rotation and Rotate -90 degrees by X axis
        bpy.ops.object.transform_apply(rotation = True) 
        bpy.ops.transform.rotate(value = 1.5708, axis = (1, 0, 0), constraint_axis = (True, False, False), constraint_orientation = 'GLOBAL')
        
        #Deletes all Materials from selected object 
        obj = bpy.context.active_object
        materials = obj.data.materials
        materials.clear(1)             

        #Cleans all Textures from texture list (Work in Progress)

        imgs = bpy.data.images
        for image in imgs:
            name = image.name
            if name[:4] != "keep":
                image.user_clear()
        
        ob = bpy.context.active_object
        me = ob.data
        
        img = bpy.data.images['XXXX'] #replace XXXX with wanted texture
        
        for uv_tex_face in me.uv_textures.active.data:
            uv_tex_face.image = img
        
        #Switch renderer to Blender Render
        bpy.context.scene.render.engine = 'BLENDER_RENDER'
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.area.type == 'VIEW_3D'
    
    def execute(self, context):
        self.applyRotScaleDelMatTex()
        return {'FINISHED'}

#Resets selected object Rotation to 0
class resetObjRotation(bpy.types.Operator):
    bl_label = "Rotation to 0"
    bl_idname = "object.rotation_to_zero"
    bl_options = {'REGISTER','UNDO'}
    
    def resetRotation(self):
        bpy.context.object.rotation_euler[0] = 0 #Rotation X
        bpy.context.object.rotation_euler[1] = 0 #Rotation Y
        bpy.context.object.rotation_euler[2] = 0 #Rotation Z
        
        
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.area.type == 'VIEW_3D'
    
    def execute(self, context):
        self.resetRotation()
        return {'FINISHED'}
    
#Resets selected object Location to 0
class  resetObjLocation(bpy.types.Operator):
    bl_label = "Location to 0"
    bl_idname = "object.location_to_zero"
    bl_options = {'REGISTER','UNDO'}
    
    def resetLocation(self):
        bpy.context.object.location[0] = 0 #Rotation X
        bpy.context.object.location[1] = 0 #Rotation Y
        bpy.context.object.location[2] = 0 #Rotation Z
        
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.area.type == 'VIEW_3D'
    
    def execute(self, context):
        self.resetLocation()
        return {'FINISHED'}
        
#Saves blend file and Refresh it to check addon worked correctly
class  saveAndRevert(bpy.types.Operator):
    bl_label = "Save File and Refresh"
    bl_idname = "object.save_file_and_refresh"
    bl_options = {'REGISTER','UNDO'}
   
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        bpy.ops.wm.save_mainfile(check_existing=True)
        bpy.ops.wm.revert_mainfile(use_scripts=True)
        return {'FINISHED'}
        
#Creates panel to toolself and buttons in it
class AddonPanel(bpy.types.Panel):
    
    bl_idname = "OBJECT_PT_checks_for_unity_applier"
    bl_label = "Check addon for Unity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"

    def draw(self, context):
        
        layout = self.layout
        
        #Button for Check
        """
        Includes:
            Apply Rotation and scale
            Rotates first -90 degree by X axis
            Apply Rotation again
            Rotates 90 degree by X axis
            Unlink all Textures and materials                    
        """
        col = layout.column(align=True)
        col.operator("object.rot_scale_check", text = "Check for Unity", icon = "MESH_MONKEY")
       
        #Layout for Rotation and Location clear to 0 buttons
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="PosRot Clear:")
        col.operator("object.rotation_to_zero", text = "Rotation Clear", icon = "FILE_REFRESH")
        col.operator("object.location_to_zero", text = "Location Clear", icon = "FULLSCREEN_ENTER")
        
        #Layout for Save and Reset
        layout = self.layout
        col = layout.column(align=True)
        col.label(text = "Save and reset File")
        col.operator("object.save_file_and_refresh", text = "Save and Reset", icon = "FILE_TICK")

#Registers for Addon
def register():
    bpy.utils.register_class(RotScaleMatTexFix)
    bpy.utils.register_class(resetObjRotation)
    bpy.utils.register_class(resetObjLocation)
    bpy.utils.register_class(saveAndRevert)
    bpy.utils.register_class(AddonPanel)
    
def unregister():
    bpy.utils.unregister_class(RotScaleMatTexFix)
    bpy.utils.unregister_class(resetObjRotation)
    bpy.utils.unregister_class(resetObjLocation)
    bpy.utils.unregister_class(saveAndRevert)
    bpy.utils.unregister_class(AddonPanel)
    
if __name__ == "__main__":
    register()
        
   