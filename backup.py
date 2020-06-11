from model.texture import *
from model.obj import *
from renderer import *
import glm
from glfw.GLFW import glfwSetCursor, glfwSetCursorPos
from Display import *
from OpenGL.GL import *
from model.loader import *
from shader import *
from tool.mmath import *
from camera import *
import glfw
import numpy as np
from pynput import keyboard

WIDTH = 1366
HEIGHT = 768

display = Display()


def gridGen(size, blocksize):
    w, h = size
    bs = blocksize
    w = int(w/bs)
    h = int(h/bs)
    out = []
    vout = []
    for i in range(h+bs):
        a = []
        b = []
        for j in range(w+bs):
            a.append([i, j, 0])
            b.append(i)
            b.append(j)
            b.append(0)
        [out.append(e) for e in a]
        [vout.append(e) for e in b]
    iout = []
    for i in range(h):
        for j in range(w):
            iout.append(out.index([i, j, 0]))
            iout.append(out.index([i, j+1, 0]))
            iout.append(out.index([i+1, j, 0]))
            iout.append(out.index([i, j+1, 0]))
            iout.append(out.index([i+1, j, 0]))
            iout.append(out.index([i+1, j+1, 0]))
    return vout, iout


gridGen((2, 2), 1)

gridData, gridIndices = gridGen((2, 2), 1)

gridData = [e/4 for e in gridData]

data = [
    -0.5, -0.5, 0.0,  # 0 Bottom Left
    -0.5,  0.5, 0.0,  # 1 Top Left
    0.5,  0.5, 0.0,  # 2 Top Right
    0.5, -0.5, 0.0  # 3 Bottom Right
]

indices = [
    0, 1, 2,
    2, 0, 3
]

line_indices = [
    0, 1,
    1, 2,
    2, 3,
    3, 0
]
data = np.array(data, dtype=np.float32)
indices = np.array(indices, dtype=np.int32)
line_indices = np.array(line_indices, dtype=np.int32)
print(data)

cameraZ = 0.0


def main():
    window = display.create(WIDTH, HEIGHT, 'GL')
    shader = Shader()
    camera = Camera(window, glm.vec3(0.0, 0.0, 1.1),
                    0.0, 0.0, 0.0, 60, 0.01, -1000)
    shader.start()
    shader.putVecInUniformLocation('color', glm.vec4(0.01, 1.0, 0.01, 1.0))

    proj = camera.createProjectionMatrix()
    shader.loadProjectionMatrix(glm.value_ptr(proj))

    view = camera.createViewMatrix()
    shader.loadViewMatrix(glm.value_ptr(view))

    vb = glGenBuffers(1)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, vb)
    glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    ivb = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ivb)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    while display.isNotClosed():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.0, 0.03, 1.0)
        shader.loadTransformationMatrix(glm.value_ptr(
            createTransformationMatrix(
                glm.vec3(0.0, 0.0, -0.1),
                glm.vec3(0.0, 0.1*glfw.get_time(), 0.0*glfw.get_time()),
                glm.vec3(1.0, 1.0, 1.0)
            )
        ))
        camera.movement()
        shader.loadViewMatrix(glm.value_ptr(camera.createViewMatrix()))
        glPointSize(3.0)
        glDrawElements(GL_TRIANGLES, len(indices)+1, GL_UNSIGNED_INT, None)
        display.update()
    shader.stop()
    glDeleteBuffers(1, [vb])
    display.close()


if __name__ == '__main__':
    main()


# --------------------------------------------------------------------------------------------------------

WIDTH = 1366
HEIGHT = 768

display = Display()


def gridGen(size, blocksize):
    w, h = size
    bs = blocksize
    w = int(w/bs)
    h = int(h/bs)
    out = []
    vout = []
    for i in range(h+bs):
        a = []
        b = []
        for j in range(w+bs):
            a.append([i, j, 0])
            b.append(i)
            b.append(j)
            b.append(0)
        [out.append(e) for e in a]
        [vout.append(e) for e in b]
    iout = []
    for i in range(h):
        for j in range(w):
            iout.append(out.index([i, j, 0]))
            iout.append(out.index([i, j+1, 0]))
            iout.append(out.index([i+1, j, 0]))
            iout.append(out.index([i, j+1, 0]))
            iout.append(out.index([i+1, j, 0]))
            iout.append(out.index([i+1, j+1, 0]))
    return vout, iout


data = [
    -0.5, -0.5, 0.0,  # 0 Bottom Left
    -0.5,  0.5, 0.0,  # 1 Top Left
    0.5,  0.5, 0.0,  # 2 Top Right
    0.5, -0.5, 0.0  # 3 Bottom Right
]

indices = [
    0, 1, 2,
    2, 0, 3
]

line_indices = [
    0, 1,
    1, 2,
    2, 3,
    3, 0
]
data = np.array(data, dtype=np.float32)
indices = np.array(indices, dtype=np.int32)
line_indices = np.array(line_indices, dtype=np.int32)

cameraZ = 0.0


def main():
    window = display.create(WIDTH, HEIGHT, 'GL')
    shader = Shader()
    glfwSetCursorPos(window, WIDTH/2, HEIGHT/2)
    camera = Camera(window, glm.vec3(0.0, 0.0, 1.1),
                    0.0, 0.0, 0.0, 60, 0.01, -1000)
    renderer = Renderer(camera, window)
    loader = Loader()
    obj = OBJ('dummy.obj')
    entity = Entity(
        #loader.loadModel(obj.loadObj(), 'tex5.jpg'),
        loader.loadRaw(data, indices),
        glm.vec3(1.0, 0.0, -1.1),
        glm.vec3(0.0, 0.0, 0.0),
        glm.vec3(1.0, 1.0, 1.0),
        mode='FILL'
    )
    entity0 = Entity(
        loader.loadModel(obj.loadObj(), 'tex3.jpg'),
        glm.vec3(0.0, 0.0, -1.0),
        glm.vec3(0.0, 0.0, 0.0),
        glm.vec3(1.0, 1.0, 1.0),
        mode='FILL',
        color=glm.vec4(1.0, 1.0, 0.0, 0.3)
    )
    renderer.process(entity, shader, hasIndex=True)
    while display.isNotClosed():
        renderer.render()
        display.update()
    display.close()


if __name__ == '__main__':
    main()
