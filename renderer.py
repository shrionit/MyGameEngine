from glfw.GLFW import *
from OpenGL.GL import *
from model.loader import *
from model.model import *
from shader import *
from tool.mmath import *
from tool.gui import *
import cv2
from PIL import Image

data = [
    1.0,  1.0, 1.0,  # 0 Bottom Left
    1.0, -1.0, 1.0,  # 1 Top Left
    -1.0, -1.0, 1.0,  # 2 Top Right
    -1.0,  1.0, 1.0  # 3 Bottom Right
]

# data = [e/2.0 for e in data]

indices = [
    0, 1, 2,
    2, 0, 3
]

texcord = [
    1.0, 1.0,  # 0
    1.0, 0.0,  # 1
    0.0, 0.0,  # 2
    0.0, 1.0,  # 3
]

data = np.array(data, dtype=np.float32)
indices = np.array(indices, dtype=np.int32)
texcord = np.array(texcord, dtype=np.float32)

shaderProp = {
    'damp': 10,
}

loader = Loader()
cv = cv2.VideoCapture(0)


class Renderer:
    def __init__(self, camera, window, impl):
        self.camera = camera
        self.projection = camera.createProjectionMatrix()
        self.window = window
        self.window_width, self.window_height = glfwGetWindowSize(self.window)
        self.entities = 0
        self.shader = 0
        self.hasIndex = False
        self.framebuffer = glGenFramebuffers(1)
        self.renderbuffer = glGenRenderbuffers(1)
        self.framebuffer_attachment = glGenTextures(1)
        self.initFrameBuffer()
        self.viewer = impl
        self.viewer.newframe(self.framebuffer_attachment)

    def initFrameBuffer(self):
        # binding frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        # binding attachment texture
        glBindTexture(GL_TEXTURE_2D, self.framebuffer_attachment)
        # binding render buffer (a direct rendered frame storage without conversion to img format)
        glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.window_width, self.window_height,
                     0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # glTexImage2D(
        #     GL_TEXTURE_2D, 0, GL_DEPTH24_STENCIL8, self.window_width, self.window_height, 0,
        #     GL_DEPTH_STENCIL, GL_UNSIGNED_INT, None
        # )
        glBindTexture(GL_TEXTURE_2D, 0)
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.framebuffer_attachment, 0)

        glRenderbufferStorage(
            GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.window_width, self.window_height)

        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        glFramebufferRenderbuffer(
            GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.renderbuffer)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR: Frame Buffer is Not complete")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def process(self, entities: Entity, shader: Shader, hasIndex=False, bgcolor=glm.vec4(0.1, 0.1, 0.1, 1.0)):
        self.scene_shader = Shader('scene_frag', 'scene_vert')
        self.scene_shader.attach()
        print('Program LOG: \n', glGetProgramInfoLog(
            self.scene_shader.shaderProgram))
        self.scene = loader.loadRaw(
            data, indices, texture=self.framebuffer_attachment, texcoord=texcord, vert_size=3)
        self.scene_shader.detach()
        self.entities = entities
        self.shader = shader
        self.hasIndex = hasIndex
        self.shader.attach()
        self.shader.loadProjectionMatrix(self.projection)
        self.bgcolor = bgcolor
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glCullFace(GL_BACK)

    def assignCamToTex(self, texid):
        ret, frame = cv.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        newimage = Image.fromarray(img)
        newimg_data = newimage.transpose(
            Image.FLIP_TOP_BOTTOM).convert('RGBA').tobytes()
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, newimage.width,
                     newimage.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, newimg_data)

    def processinput(self):
        if glfwGetKey(self.window, eval('GLFW_KEY_UP')) == GLFW_PRESS:
            shaderProp['damp'] += 1
            self.shader.putSingleValueAt('damp', shaderProp['damp'])
        if glfwGetKey(self.window, GLFW_KEY_DOWN) == GLFW_PRESS:
            shaderProp['damp'] -= 1
            self.shader.putSingleValueAt('damp', shaderProp['damp'])

    def renderframe(self):
        glEnable(GL_CULL_FACE)
        self.shader.attach()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.projection = self.camera.createProjectionMatrix()
        self.shader.loadProjectionMatrix(self.projection)
        glClearColor(*self.bgcolor)
        self.processinput()
        for entity in self.entities:
            self.shader.putDataInUniformLocation('color', entity.model.color)
            view = self.camera.createViewMatrix()
            self.shader.loadViewMatrix(glm.value_ptr(view))
            self.camera.movement()
            trans = entity.updatemat(createTransformationMatrix)
            self.shader.loadTransformationMatrix(glm.value_ptr(
                trans
            ))
            if self.shader._default_frag != entity.entity_shader:
                self.shader.updateShader(entity.entity_shader)
            entity.bind()
            if entity.id == 'dummy':
                entity.setrotation(glm.vec3(0.0, 0.2*glfwGetTime(), 0.0))
                entity.updateTex(self.framebuffer_attachment)
            mode = entity.getmode()
            if mode == 'WIRE':
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                mode = GL_TRIANGLES
            elif mode == 'VERT':
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                glPointSize(3.0)
                mode = GL_POINTS
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                mode = GL_TRIANGLES

            if not self.hasIndex:
                glDrawArrays(
                    mode, 0, entity.getmodel().v_count()
                )
            else:
                glDrawElements(
                    mode, entity.getmodel().i_count(),
                    GL_UNSIGNED_INT, None
                )
            entity.unbind()

    def renderscene(self):
        glEnable(GL_FRAMEBUFFER_SRGB)
        glDisable(GL_CULL_FACE)
        self.scene_shader.attach()
        self.scene.bind()
        # for i in range(len(GUI_STATE.kernelprop.data)):
        #     self.scene_shader.putDataInUniformLocation(
        #         f'kernel[{i}]', eval(f'GUI_STATE.kernelprop.data[{i}]'))

        self.scene_shader.putDataInUniformLocation(
            'gamma', [GUI_STATE.renderprop.gamma])
        glDisable(GL_DEPTH_TEST)
        glDrawElements(
            GL_TRIANGLES, self.scene.i_count(),
            GL_UNSIGNED_INT, None
        )
        self.viewer.show()
        self.scene.unbind()
        glEnable(GL_DEPTH_TEST)

    def dispose(self):
        self.scene_shader.stop()
        self.shader.stop()
