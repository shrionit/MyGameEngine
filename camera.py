from math import *

import glfw as g
import keyboard
import mouse
import pyrr
from glfw import set_window_should_close
from glfw.GLFW import *
from glfw.GLFW import glfwSetInputMode
from PIL import Image

import glm
import Input as m


def lerp(a, b, t):
    return (1-t)*a + t*b


def rot(t):
    if t < 0:
        return lerp(0, -math.pi*2, -t)
    else:
        return lerp(0, math.pi*2, t)


class Camera:

    def __init__(self, window, pos, fov, nearZ, farZ, sensitivity=0.25):
        '''
        Takes -
                window :window object
                pos    :glm::vec3 camera position
                fov    :fov camera view angle in degrees
                nearZ  :nearPlane Z-axis value
                farZ   :farPlane Z-axis value

        '''
        self.pos = pos
        self.target = glm.vec3(0.0, 0.0, 0.0)
        self.pitch = 0.0
        self.yaw = -90.0
        self.roll = 0.0
        self.sensitivity = sensitivity
        self.window = window
        self.screenwidth, self.screenheight = g.get_window_size(self.window)
        self.lastX, self.lastY = self.screenwidth/2, self.screenheight/2
        self.fov = fov
        self.flag = False
        self.firstmouse = True
        self.nearZ, self.farZ = nearZ, farZ
        self.deltaTime = 0.0
        self.lastFrame = 0.0
        self.cameraFront = glm.vec3(0.0, 0.0, -1.0)
        self.cameraUp = glm.vec3(0.0, 1.0, 0.0)
        self.cameraRight = glm.vec3(1.0, 0.0, 0.0)
        self.counter = 0
        self.i = 0
        self.cursor_show = True
        glfwSetInputMode(self.window, GLFW_CURSOR,
                         GLFW_CURSOR_DISABLED)

    def setwindowsize(self, window, w, h):
        self.screenwidth = w
        self.screenheight = h

    def movement(self):
        self.currentFrame = glfwGetTime()
        self.deltaTime = self.currentFrame - self.lastFrame
        self.keyhandler(self.deltaTime)
        self.lastFrame = self.currentFrame
        glfwSetScrollCallback(self.window, self.scroll_handler)
        glfwSetWindowSizeCallback(self.window, self.setwindowsize)
        g.set_cursor_enter_callback(self.window, self.mouse_entered)
        glfwSetCursorPosCallback(self.window, self.mousehandler)

    def mouse_entered(self, *args):
        self.flag = True if args[1] == 1 else False
        self.firstmouse = self.flag

    def scroll_handler(self, window, xoff, yoff):
        self.fov -= yoff
        if self.fov < 1.0:
            self.fov = 1.0
        if self.fov > 75.0:
            self.fov = 75.0

    def mousehandler(self, window, x, y):
        if self.firstmouse:
            self.lastX = x
            self.lastY = y
            self.firstmouse = False
        xOff = x - self.lastX
        yOff = self.lastY - y
        self.lastX = x
        self.lastY = y
        xOff *= self.sensitivity
        yOff *= self.sensitivity

        self.yaw += xOff
        self.pitch += yOff

        if self.pitch > 89:
            self.pitch = 89
        if self.pitch < -89:
            self.pitch = -89

        direction = glm.vec3(0.0, 0.0, 0.0)
        direction.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        direction.y = sin(radians(self.pitch))
        direction.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.cameraFront = glm.normalize(direction)
        self.cameraRight = glm.normalize(
            glm.cross(self.cameraFront, glm.vec3(0.0, 1.0, 0.0)))
        self.cameraUp = glm.normalize(
            glm.cross(self.cameraRight, self.cameraFront))

    def keyhandler(self, speed_m=1.0):
        self.cameraSpeed = 2.5 * speed_m
        if self.flag:
            if glfwGetKey(self.window, GLFW_KEY_W) == GLFW_PRESS:  # W
                self.pos += self.cameraSpeed * self.cameraFront
                #self.move(0, 0, -0.01)
            if glfwGetKey(self.window, GLFW_KEY_S) == GLFW_PRESS:  # S
                self.pos -= self.cameraSpeed * self.cameraFront
                #self.move(0, 0, 0.01)
            if glfwGetKey(self.window, GLFW_KEY_A) == GLFW_PRESS:  # A
                self.pos -= glm.normalize(glm.cross(self.cameraFront,
                                                    self.cameraUp)) * self.cameraSpeed
            if glfwGetKey(self.window, GLFW_KEY_D) == GLFW_PRESS:  # D
                self.pos += glm.normalize(glm.cross(self.cameraFront,
                                                    self.cameraUp)) * self.cameraSpeed
            if glfwGetKey(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:  # ESC
                g.set_window_should_close(self.window, True)

            if glfwGetKey(self.window, GLFW_KEY_LEFT_CONTROL) == GLFW_PRESS:  # ESC
                self.i += 1

            if self.i > 5:
                glfwSetInputMode(self.window, GLFW_CURSOR,
                                 GLFW_CURSOR_NORMAL)
                if self.i > 10:
                    self.i = 0
            else:
                glfwSetInputMode(self.window, GLFW_CURSOR,
                                 GLFW_CURSOR_DISABLED)

    def move(self, x, y, z):
        self.pos.x += x
        self.pos.y += y
        self.pos.z += z

    def createProjectionMatrix(self, fov=False, ratio=False):
        return pyrr.matrix44.create_perspective_projection_matrix(
            self.fov if not fov else fov,
            self.screenwidth/self.screenheight if not ratio else ratio,
            self.nearZ,
            self.farZ
        )

    def createViewMatrix(self):
        return glm.lookAt(
            self.pos,
            self.pos + self.cameraFront,
            self.cameraUp
        )

    def setPos(self, npos):
        self.pos = npos

    def setPitch(self, pitch):
        self.pitch = pitch

    def setYaw(self, yaw):
        self.yaw = yaw

    def setRoll(self, roll):
        self.roll = roll

    def getPos(self):
        return self.pos

    def getPitch(self):
        return self.pitch

    def getYaw(self):
        return self.yaw

    def getRoll(self):
        return self.roll
