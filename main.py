import glfw
from OpenGL.GL import *
from model.obj import *
from model.loader import *
from Display import *
from shader import *
from camera import *
from renderer import *
import glm
#-------------------------------------------------------------------------

def createTransformationMatrix(translate, rotate, scale):
    transformation = glm.translate(glm.mat4(1.0), translate)
    transformation = glm.rotate(transformation, rotate.x, glm.vec3(1, 0, 0))
    transformation = glm.rotate(transformation, rotate.y, glm.vec3(0, 1, 0))
    transformation = glm.rotate(transformation, rotate.z, glm.vec3(0, 0, 1))
    transformation = glm.scale(transformation, scale)
    return transformation

def createProjectionMatrix(FOV, width, height, nearPlane, farPlane):
    projection = glm.perspectiveFov(glm.radians(FOV), width, height, nearPlane, farPlane)
    return projection
    
def createViewMatrix(camera):
    view = glm.rotate(glm.mat4(1.0), camera.getPitch(), glm.vec3(1, 0, 0))
    view = glm.rotate(glm.mat4(1.0), camera.getYaw(), glm.vec3(0, 1, 0))
    view = glm.rotate(glm.mat4(1.0), camera.getRoll(), glm.vec3(0, 0, 1))
    cameraPos = glm.vec3(-camera.getPos().x, -camera.getPos().y, -camera.getPos().z)
    view = glm.translate(view, cameraPos)
    return view

def main():
    display = Display()
    window = display.create(1366, 768, 'MYWINDOW')
    
    shader = Shader()
    shader.start()
    shader.getAllUniformLocations()
    shader.getUniformLocationOfVariable('position')
    
    camera = Camera(window, glm.vec3(0.0, 0.0, 1.0), 0.0, 0.0, 0.0, 75,  0.1, -1000)
    
    shader.putVec3InUniformLocation('setColor', [1.0, 0.0, 0.3])
    shader.putVec3InUniformLocation('ambientC', [1.0, 1.0, 1.0])
    p = createProjectionMatrix(75, 1366, 768, 0.1, -1000)
    shader.loadProjectionMatrix(glm.value_ptr(p))
    t = createTransformationMatrix(glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.5, 0.0, 0.0), glm.vec3(1.0, 1.0, 1.0))
    shader.loadTransformationMatrix(glm.value_ptr(t))
    
    
    obj = OBJ('dummy.obj').loadObj()
    load = Loader()
    model = load.loadModel(obj, 'grey.png')
    entity = Entity(model, glm.vec3(0.0, 0.0, -2.0), glm.vec3(0.0, 0.0, 0.0), glm.vec3(1.0, 1.0, 1.0))
    renderer = Renderer(shader, camera)
    
    glBindVertexArray(entity.gettexturedmodel().getModel().getID())
    glBindTexture(GL_TEXTURE_2D, entity.gettexturedmodel().getTexture().getTexID())
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    pos = glm.vec3(0.0, 0.0, -10.0)
    while display.isNotClosed():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        rot = glm.vec3(0.0, 0.5*glfw.get_time(), 0.0)
        t = createTransformationMatrix(
            entity.getposition(),
            rot,
            entity.getscale()
            )
        camera.movement()
        v = createViewMatrix(camera)
        shader.loadViewMatrix(glm.value_ptr(v))
        shader.loadTransformationMatrix(glm.value_ptr(t))
        renderer.render(entity)
        #glDrawElements(GL_TRIANGLES, entity.gettexturedmodel().getModel().getCount()+1, GL_UNSIGNED_INT, None)
        
        display.update()
        
    
    display.close()


if __name__ == '__main__':
    main()
