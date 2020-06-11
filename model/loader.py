from OpenGL.GL import *
from model.texture import *
from model.obj import *
from model.model import *
import numpy as np
from PIL import Image

TEXCORD = np.array([
    0.0, 1.0,
    1.0, 1.0,
    0.0, 0.0,
    1.0, 0.0
], dtype=np.float32)


def genNormals(count):
    a = []
    for i in range(count):
        a += [0, 0, 1]
    return np.array(a, dtype=np.float32)


def convColor(color):
    return [int(e*255) for e in color]


class Loader:
    def __init__(s):
        s.vaos = []
        s.vbos = []

    def loadRaw(s, vertices, indices=[], texture=[0.0, 0.0, 0.0, 1.0], texcoord=[], vert_size=3):
        tex = 0
        if type(texture) == list:
            tex = Texture(Image.new('RGBA', (28, 28),
                                    tuple(convColor(texture))), isimg=True).getTexID()
        else:
            tex = texture
        norm = genNormals(len(vertices))
        modelVAO = s.createVAO()
        s.loadDataInVAOsAttribNumer(0, vertices, vert_size)
        s.loadDataInVAOsAttribNumer(1, norm, 3)
        s.loadDataInVAOsAttribNumer(
            2, TEXCORD if len(texcoord) == 0 else texcoord, 2)
        s.loadIndices(indices)
        glBindVertexArray(0)
        rmodel = RawModel(modelVAO, len(vertices))
        return TexturedModel(rmodel, tex, len(indices))

    def loadModel(s, model, texture):
        s.tex = Texture(texture).getTexID() if type(texture) is str else Texture(
            Image.new('RGBA', (28, 28), tuple(convColor(texture))), isimg=True).getTexID()
        modelVAO = s.createVAO()
        s.loadDataInVAOsAttribNumer(0, model['vertex'], 3)
        s.loadDataInVAOsAttribNumer(1, model['normal'], 3)
        s.loadDataInVAOsAttribNumer(2, model['texture'], 2)
        s.loadIndices(model['index'])
        glBindVertexArray(0)
        rmodel = RawModel(modelVAO, model['count'])
        tmodel = TexturedModel(rmodel, s.tex, len(model['index']))
        return tmodel

    def loadDataInVAOsAttribNumer(s, attribN, data, pair):
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glEnableVertexAttribArray(attribN)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        glVertexAttribPointer(attribN, pair, GL_FLOAT, GL_FALSE, 0, None)
        s.vbos.append(vbo)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def loadIndices(s, data):
        ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        return ibo

    def createVAO(s):
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        s.vaos.append(vao)
        return vao

    def cleanUP(s):
        for e in s.vaos:
            glDeleteVertexArrays(e)
        glDeleteBuffers(s.vbos)
