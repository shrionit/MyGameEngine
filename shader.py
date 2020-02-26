import os

from abc import ABC
from abc import abstractmethod

from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm

class Shader(ABC):

    def __init__(self):
        self.shaderVertex = compileShader(self.loadShader('vertex'), GL_VERTEX_SHADER)
        self.shaderFragment = compileShader(self.loadShader('fragment'), GL_FRAGMENT_SHADER)
        self.shaderProgram = compileProgram(self.shaderVertex, self.shaderFragment)
        #self.getAllUniformLocations()
        self.uniformLocations = []

    def start(self):
        for l in self.uniformLocations:
            glVertexAttribPointer(l, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(l)
        
        
        glUseProgram(self.shaderProgram)
        self.location_color = glGetUniformLocation(self.shaderProgram, 'setColor')
        

    def stop(self):
        glUseProgram(0)
        glDeleteShader(self.shaderVertex)
        glDeleteShader(self.shaderFragment)
        

    def loadShader(self, name):
        read = open(os.getcwd()+'\\shaderfiles\\'+name+'.'+name[0:4], 'r')
        return read.read()

    def getAllUniformLocations(self):
        self.location_color = glGetAttribLocation(self.shaderProgram, 'setColor')
        

    def getUniformLocationOfVariable(self, name):
        self.uniformLocations.append(glGetUniformLocation(self.shaderProgram, name))
        
    
    def kindOfDataStoredInPosition(self, position, NumberOfPoints):
        glVertexAttribPointer(position, NumberOfPoints, GL_FLOAT, GL_FALSE, 0, None)

    def putVec3InUniformLocation(self, location, vec3data):
        loc = glGetUniformLocation(self.shaderProgram, location)
        glUniform3f(loc, vec3data[0], vec3data[1], vec3data[2])

    def loadViewMatrix(self, matrix_view):
        self.location_viewMatrix = glGetUniformLocation(self.shaderProgram, 'viewMatrix')
        glUniformMatrix4fv(self.location_viewMatrix, 1, GL_FALSE, matrix_view)

    def loadTransformationMatrix(self, matrix_transformation):
        self.location_transformationMatrix = glGetUniformLocation(self.shaderProgram, 'transformationMatrix')
        glUniformMatrix4fv(self.location_transformationMatrix, 1, GL_FALSE, matrix_transformation)

    def loadProjectionMatrix(self, matrix_projection):
        self.location_projectionMatrix = glGetUniformLocation(self.shaderProgram, 'projectionMatrix')
        glUniformMatrix4fv(self.location_projectionMatrix, 1, GL_FALSE, matrix_projection)
        
