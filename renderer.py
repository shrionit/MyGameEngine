from OpenGL.GL import *
from OpenGL.GL.shaders import *
from camera import *
from shader import *
class Renderer:
    def __init__(self,shader, camera):
        self.shader = shader
        self.camera = camera
    
    def render(self, entity, shader=None):
        if shader:
            self.shader = shader
        
        glUseProgram(self.shader)
        
        glBindVertexArray(entity.gettexturedmodel().getModel().getID())
        glBindTexture(GL_TEXTURE_2D, entity.gettexturedmodel().getTexture().getTexID())
        
        glDrawElements(GL_TRIANGLES, entity.gettexturedmodel().getModel().getCount(), GL_UNSIGNED_INT, None)
        glUseProgram(0)