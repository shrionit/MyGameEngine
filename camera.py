import keyboard
import Input as m
import glfw as g
import glm
import mouse
class Camera:

    def __init__(self, window, pos, pitch, yaw, roll, fov, nearZ, farZ):
        self.pos = pos
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.window = window
        self.screenwidth, self.screenheight = g.get_window_size(self.window)
        self.FOV = fov
        self.nearZ, self.farZ = nearZ, farZ
    
    def movement(self):
        keyboard.add_hotkey('left', lambda: self.move(0.0001, 0, 0))
        keyboard.add_hotkey('right', lambda: self.move(-0.0001, 0, 0))
        keyboard.add_hotkey('w', lambda: self.move(0, 0.0001, 0))
        keyboard.add_hotkey('s', lambda: self.move(0, -0.0001, 0))   
        m.onscroll(self.window, self.zoom)

    def zoom(self, e):
        print(e.delta)
        if isinstance(e, mouse.WheelEvent):
            d = e.delta
            if d > 0:
                self.move(0, 0, -0.001)
            elif d < 0:
                self.move(0, 0, 0.001)

    def move(self, x, y, z):
        self.pos.x += x
        self.pos.y += y
        self.pos.z += z

    def createProjectionMatrix(self):
        projection = glm.perspectiveFov(glm.radians(self.FOV), self.screenwidth, self.screenheight, self.nearZ, self.farZ)
        return projection
        
    def createViewMatrix(self):
        view = glm.rotate(glm.mat4(1.0), self.getPitch(), glm.vec3(1, 0, 0))
        view = glm.rotate(glm.mat4(1.0), self.getYaw(), glm.vec3(0, 1, 0))
        view = glm.rotate(glm.mat4(1.0), self.getRoll(), glm.vec3(0, 0, 1))
        cameraPos = glm.vec3(-self.getPos().x, -self.getPos().y, -self.getPos().z)
        view = glm.translate(view, cameraPos)
        return view

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