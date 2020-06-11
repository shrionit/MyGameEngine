import glm
import numpy as np
from pyrr import *


def createTransformationMatrix(translate, rotate, scale):
    ''' Takes - 
                translate :glm::vec3
                rotate :glm::vec3
                scale :glm.vec3
    '''
    transformation = glm.translate(glm.mat4(1.0), translate)
    transformation = glm.rotate(transformation, rotate.x, glm.vec3(1, 0, 0))
    transformation = glm.rotate(transformation, rotate.y, glm.vec3(0, 1, 0))
    transformation = glm.rotate(transformation, rotate.z, glm.vec3(0, 0, 1))
    transformation = glm.scale(transformation, scale)
    return transformation


def createProjectionMatrix(FOV, width, height, nearPlane, farPlane):
    ''' Takes - 
                FOV :view angle in degrees
                width :display width
                height :display height
                nearPlane :nearPlane distance from camera
                farPlane :farPlane distance from camera
    '''
    projection = pyrr.Matrix44.create_perspective_projection_matrix(
        60, width/height, nearPlane, farPlane)
    return projection


def createViewMatrix(camera):
    ''' Takes - 
                camera: Camera Object
    '''
    view = glm.rotate(glm.mat4(1.0), camera.getPitch(), glm.vec3(1, 0, 0))
    view = glm.rotate(glm.mat4(1.0), camera.getYaw(), glm.vec3(0, 1, 0))
    view = glm.rotate(glm.mat4(1.0), camera.getRoll(), glm.vec3(0, 0, 1))
    cameraPos = glm.vec3(-camera.getPos().x, -
                         camera.getPos().y, -camera.getPos().z)
    view = glm.translate(view, cameraPos)
    return view
