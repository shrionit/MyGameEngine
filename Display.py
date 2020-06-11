import glfw
import keyboard
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import Input
from tool.gui import *


class Display:
    def __init__(self):
        GUI.FONT = 'VarelaRound-Regular.ttf'
        GUI.FONT_SIZE = 30
        if not glfw.init():
            return

    def create(self, W, H, TITLE):
        self.window = glfw.create_window(W, H, TITLE, None, None)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        if not self.window:
            glfw.terminate()
            return
        glfw.make_context_current(self.window)
        GUI.WINDOW = self.window
        self.gui = RenderView()
        return self.window, self.gui

    def isNotClosed(self):
        return not glfw.window_should_close(self.window)

    def update(self):
        Input.getmouse(self.window)
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def keyEvent(self, f):
        keyboard.add_hotkey('up', callback=f)

    def close(self):
        self.gui.shutdown()
        glfw.terminate()
