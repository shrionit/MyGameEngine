import glfw
import keyboard
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import Input

class Display:
    def __init__(self):
        if not glfw.init():
            return
    
    def create(self, W, H, TITLE):
        self.window = glfw.create_window(W, H, TITLE, None, None)
        if not self.window:
            glfw.terminate()
            return
        glfw.make_context_current(self.window)
        return self.window

    def isNotClosed(self):
        return not glfw.window_should_close(self.window)
    
    def update(self):
        Input.getmouse(self.window)
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        
    def keyEvent(self, f):
        keyboard.add_hotkey('up', callback=f)
    
    def close(self):
        glfw.terminate()
