import glfw
import numpy as np
from glfw.GLFW import glfwSetCursor, glfwSetCursorPos
from OpenGL.GL import *
from pynput import keyboard
import glm

from camera import *
from Display import *
from model.loader import *
from renderer import *
from shader import *
from model.obj import *
from model.texture import *
from tool.mmath import *
from tool.color import Color

WIDTH = 1366
HEIGHT = 768

display = Display()
# imgui.create_context()

line_indices = [
    0, 1,
    1, 2,
    2, 3,
    3, 0
]
line_indices = np.array(line_indices, dtype=np.int32)

cameraZ = 0.0


def main():
    window, impl = display.create(WIDTH, HEIGHT, 'GL')
    shader = Shader()
    print(f'Main shader program = {shader.shaderProgram}')
    # glfwSetCursorPos(window, WIDTH/2, HEIGHT/2)
    camera = Camera(window, glm.vec3(0.0, 0.0, 3.0), 75, 0.1, 1000, 0.5)
    renderer = Renderer(camera, window, impl)
    loader = Loader()
    color = '#F24405'
    entities = [
        Entity(
            'plane',
            loader.loadModel(OBJ('plane.obj').loadObj(),
                             Color(115, 133, 140)),
            glm.vec3(0.0, -1.0, 0.0),
            glm.vec3(0.0, 0.0, 0.0),
            glm.vec3(1.0, 1.0, 1.0),
            mode='FILL'
        ),
        Entity(
            'dummy',
            loader.loadModel(OBJ('dummy.obj').loadObj(), Color(34, 52, 64)),
            glm.vec3(-2.0, 0.0, 0.0),
            glm.vec3(0.0, 0.0, 0.0),
            glm.vec3(1.0, 1.0, 1.0),
            mode='FILL'
        ),
        Entity(
            'cube',
            loader.loadModel(OBJ('cube.obj').loadObj(), 'tex5.jpg'),
            #loader.loadRaw(data, indices, color=glm.vec4(1.0, 0.0, 1.0, 1.0)),
            glm.vec3(0.0, 0.0, -2.0),
            glm.vec3(0.0, 0.0, 0.0),
            glm.vec3(1.0, 1.0, 1.0),
            mode='FILL',
        ),
        Entity(
            'sphere',
            loader.loadModel(OBJ('sphere.obj').loadObj(),
                             Color(242, 68, 5)),
            #loader.loadRaw(data, indices, color=glm.vec4(1.0, 0.0, 1.0, 1.0)),
            glm.vec3(2.0, 0.0, 0.0),
            glm.vec3(0.0, 0.0, 0.0),
            glm.vec3(1.0, 1.0, 1.0),
            mode='FILL',
        ),
    ]

    renderer.process(entities, shader, hasIndex=True)
    while display.isNotClosed():
        glBindFramebuffer(GL_FRAMEBUFFER, renderer.framebuffer)
        renderer.renderframe()  # main rendering
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        renderer.renderscene()  # main rendering
        display.update()
    renderer.dispose()
    display.close()


if __name__ == '__main__':
    main()
