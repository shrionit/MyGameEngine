class RawModel:
    def __init__(self, vao, vertexCount):
        self.vaoID = vao
        self.vertexCount = vertexCount
    
    def getID(self):
        return self.vaoID
    
    def getCount(self):
        return self.vertexCount

class TexturedModel:
    def __init__(self, model, texture):
        self.model = model
        self.texture = texture
        
    def getModel(self):
        return self.model
    
    def getTexture(self):
        return self.texture

class Entity:
    def __init__(self, texturedmodel, position, rotation, scale):
        self.tmodel = texturedmodel
        self.pos = position
        self.rot = rotation
        self.scale = scale
    
    def gettexturedmodel(self):
        return self.tmodel
    
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
