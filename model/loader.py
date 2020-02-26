from OpenGL.GL import *
from model.texture import *
from model.obj import *
from model.model import *
class Loader:
    def __init__(s):
        s.vaos = []
        s.vbos = []
    
    def loadModel(s, model, texture):
        s.tex = Texture(texture)
        modelVAO = s.createVAO()
        s.loadDataInVAOsAttribNumer(0, model['vertex'], 3)
        s.loadDataInVAOsAttribNumer(1, model['normal'], 3)
        s.loadDataInVAOsAttribNumer(2, model['texture'], 2)
        s.loadIndices(model['index'])
        glBindVertexArray(0)
        rmodel = RawModel(modelVAO, model['count'])
        tmodel = TexturedModel(rmodel, s.tex)
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
        
    def createVAO(s):
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        s.vaos.append(vao)
        return vao
    
    def cleanUP(s):
        for e in s.vaos:
            glDeleteVertexArrays(e)
        glDeleteBuffers(s.vbos)
        