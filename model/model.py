from OpenGL import *
from OpenGL.GL import *
import glm


class RawData:
    def __init__(self, vboID, vertexCount, iboID=None, indexCount=0, color=glm.vec4(1.0, 1.0, 1.0, 1.0)):
        self.vboID = vboID
        self.iboID = iboID
        self.vertexCount = vertexCount
        self.indexCount = indexCount
        self.color = color
        self.isbind = False

    def v_count(self):
        return self.vertexCount

    def i_count(self):
        return self.indexCount

    def bind(self):
        if not self.isbind:
            glBindBuffer(GL_ARRAY_BUFFER, self.vboID)
            if self.iboID:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.iboID)

    def unbind(self):
        if self.isbind:
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            if iboID:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


class RawModel:
    def __init__(self, vao, indexCount, color=glm.vec4(1.0, 1.0, 1.0, 1.0)):
        self.vaoID = vao
        self.indexCount = indexCount
        self.color = color

    def bind(self):
        glBindVertexArray(self.vaoID)

    def unbind(self):
        glBindVertexArray(0)

    def i_count(self):
        return self.indexCount


class TexturedModel:
    def __init__(self, rawmodel, textureID, indexCount):
        self.rawmodel = rawmodel
        self.vaoID = rawmodel.vaoID
        self.textureID = textureID
        self.indexCount = indexCount
        self.oldtexid = self.textureID

    def i_count(self):
        return self.indexCount

    def bind(self):
        glBindVertexArray(self.vaoID)
        glBindTexture(GL_TEXTURE_2D, self.textureID)

    def bindnew(self, newid):
        if newid != self.oldtexid:
            glBindTexture(GL_TEXTURE_2D, newid)
            self.oldtexid = newid

    def unbind(self):
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)

    def getTexture(self):
        return self.textureID


class Entity:
    def __init__(self, id, model, position, rotation, scale, mode='FILL', color=glm.vec4(1.0, 1.0, 1.0, 1.0), entity_shader='fragment'):
        '''Takes -
                    id :unique identifier
                    model :Object in [RawData, RawModel, TexturedModel]
                    position : glm::vec3
                    rotation : glm::vec3
                    scale : glm::vec3
                    mode : mode in ['WIRE', 'FILL', 'VERT']
                    color : glm::vec4
        '''
        self.id = id
        self.model = model
        self.model.color = color
        self.pos = position
        self.rot = rotation
        self.scale = scale
        self.mode = mode
        self.entity_shader = entity_shader

    def bind(self):
        self.model.bind()

    def updateTex(self, newtexid):
        self.model.bindnew(newtexid)

    def unbind(self):
        self.model.unbind()

    def updatemat(self, mat):
        return mat(self.pos, self.rot, self.scale)

    def getmode(self):
        return self.mode

    def getmodel(self):
        return self.model

    def getposition(self):
        return self.pos

    def getrotation(self):
        return self.rot

    def getscale(self):
        return self.scale

    def setposition(self, vector):
        self.pos = vector

    def setrotation(self, vector):
        self.rot = vector

    def setscale(self, vector):
        self.scale = vector


class Vertex:
    def __init__(self, *args):
        n = len(args)
        if n == 1:
            self.location = args[0]
