import glm
import numpy
class OBJ:
    def __init__(self, file):
        self.vertices = []
        self.textures = []
        self.normals = []
        self.indices = []
        with open('model\\data\\models\\'+file, 'r') as f:
            for l in f:
                l = l.strip('\n')
                ll = l.split(' ')
                if ll[0] == 'v':
                    vert = glm.vec3(float(ll[1]), float(ll[2]), float(ll[3]))
                    self.vertices.append(vert)
                elif ll[0] == 'vt':
                    tex = glm.vec2(float(ll[1]), float(ll[2]))
                    self.textures.append(tex)
                elif ll[0] == 'vn':
                    norm = glm.vec3(float(ll[1]), float(ll[2]), float(ll[3]))
                    self.normals.append(norm)
                elif ll[0] == 's':
                    self.texturesArray = [None] * len(self.vertices) * 2
                    self.normalsArray = [None] * len(self.vertices) * 3
                    break

            for l in f:
                l = l.strip('\n')
                ll = l.split(' ')
                if ll[0] == 'f':
                    for e in ll[1:]:
                        vertexData = e.split('/')
                        self.processVertex(vertexData, self.indices, self.textures, self.normals, self.texturesArray, self.normalsArray)
        
            self.vertexArray = [None] * len(self.vertices) * 3
            
            #self.indicesArray = [None] * len(self.indices)
            #print(f'after {len(self.indices)}')

            i = 0
            for e in self.vertices:
                self.vertexArray[i] = e.x
                i = i + 1
                self.vertexArray[i] = e.y
                i = i + 1
                self.vertexArray[i] = e.z
                i = i + 1
            
            

            self.indicesArray = self.indices
            
        self.vertexArray = numpy.array(self.vertexArray, dtype=numpy.float32)
        self.normalsArray = numpy.array(self.normalsArray, dtype=numpy.float32)
        self.texturesArray = numpy.array(self.texturesArray, dtype=numpy.float32)
        self.indicesArray = numpy.array(self.indicesArray, dtype=numpy.int32)
        self.model = {'vertex':self.vertexArray, 'normal':self.normalsArray, 'texture':self.texturesArray, 'index':self.indicesArray, 'count':len(self.indicesArray)}
        
        
    def processVertex(self, vertexData, indices, textures, normals, tArray, nArray):
        currentVertexPointer = int(vertexData[0])-1
        #print(vertexData)
        indices.append(currentVertexPointer)
        if vertexData[1] != '':
            c_texture = glm.vec2(textures[int(vertexData[1])-1])
            tArray[currentVertexPointer*2] = c_texture.x
            tArray[currentVertexPointer*2+1] = c_texture.y
        if vertexData[2] != '':
            c_normal = glm.vec3(normals[int(vertexData[2])-1])
            nArray[currentVertexPointer*3] = c_normal.x
            nArray[currentVertexPointer*3+1] = c_normal.y
            nArray[currentVertexPointer*3+2] = c_normal.z
            
    def loadObj(self):
        return self.model