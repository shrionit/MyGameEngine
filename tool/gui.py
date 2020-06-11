from abc import ABCMeta, abstractmethod

import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

from model.texture import Texture
import numpy as np
from PIL import Image


class O:
    pass


GUI_STATE = O()
GUI_STATE.lightprop = O()
GUI_STATE.renderprop = O()
GUI_STATE.kernelprop = O()

GUI_STATE.lightprop.isvisible = True
GUI_STATE.renderprop.isvisible = True
GUI_STATE.kernelprop.isvisible = True

GUI_STATE.lightprop.blinn = 1.0
GUI_STATE.lightprop.specDamp = 5.0
GUI_STATE.lightprop.shininess = 16.0
GUI_STATE.lightprop.shininess = 16.0

GUI_STATE.renderprop.gamma = 1.0

GUI_STATE.kernelprop.data = [[0.0, 0.0, 0.0]]*3


class GUI(GlfwRenderer, metaclass=ABCMeta):
    """docstring for GUI."""
    WINDOW = None
    FONT = 'VarelaRound-Regular.ttf'
    SCALE_FACTOR = 2
    FONT_SIZE = 30

    def __init__(self):
        imgui.create_context()
        super().__init__(GUI.WINDOW)
        imgui.get_io().fonts.get_tex_data_as_rgba32()
        self.io = imgui.get_io()

        win_w, win_h = glfw.get_window_size(GUI.WINDOW)
        fb_w, fb_h = glfw.get_framebuffer_size(GUI.WINDOW)
        # self.scale_factor = max(float(fb_w) / win_w, float(fb_h) / win_h)
        self.font = 'assets/'+GUI.FONT
        self.io.display_size = win_w, win_h
        self.new_font = self.io.fonts.add_font_from_file_ttf(
            self.font, GUI.FONT_SIZE * GUI.SCALE_FACTOR,
        )
        self.io.font_global_scale /= GUI.SCALE_FACTOR
        self.refresh_font_texture()

    def show(self):
        self.process_inputs()
        imgui.new_frame()
        self.draw()
        imgui.render()
        self.render(imgui.get_draw_data())
        imgui.end_frame()

    @abstractmethod
    def draw(self):
        pass

    def stop(self):
        imgui.end_frame()
        self.shutdown()


class RenderView(GUI):
    def __init__(self, framebufferid=0, font='', scale_factor=2, font_size=30):
        super().__init__()
        GUI_STATE.renderprop.img = framebufferid if framebufferid != 0 else Texture(
            Image.new('RGBA', (512, 512), 'BLACK'), isimg=True).getTexID()
        if font == '':
            self.font = GUI.FONT
        imgui.get_io().fonts.get_tex_data_as_rgba32()
        self.io = imgui.get_io()
        self.font = 'assets/'+self.font
        self.new_font = self.io.fonts.add_font_from_file_ttf(
            self.font, font_size*scale_factor,
        )

        win_w, win_h = glfw.get_window_size(GUI.WINDOW)
        fb_w, fb_h = glfw.get_framebuffer_size(GUI.WINDOW)
        font_scaling_factor = max(float(fb_w) / win_w, float(fb_h) / win_h)
        font_scaling_factor += 0.8
        self.io.font_global_scale /= font_scaling_factor
        self.refresh_font_texture()

    def newframe(self, id):
        GUI_STATE.renderprop.img = id

    def getdata(self, data, o=False, dtype='f'):
        return np.array([e for e in data.split() if e != '-'], dtype=np.float32)

    def draw(self):

        with imgui.font(self.new_font):
            imgui.begin("Test")
            expanded0, visible = imgui.collapsing_header(
                'Raw Scene', GUI_STATE.renderprop.isvisible)
            if expanded0:
                imgui.image(GUI_STATE.renderprop.img, 256, 256, (0, 1),
                            (1, 0), border_color=(0.5, 0.3, 0.2, 1.0))
                changed, GUI_STATE.renderprop.gamma = imgui.input_float(
                    ' : Gamma', GUI_STATE.renderprop.gamma)
            # kernel
            expanded1, visible = imgui.collapsing_header(
                'Kernel', GUI_STATE.kernelprop.isvisible)
            if expanded1:
                changed, row = imgui.input_float3(
                    ':Kernel R0', *GUI_STATE.kernelprop.data[0])
                print(f'R0 => CHANGED = {changed}, ROW = {row}')
                GUI_STATE.kernelprop.data[0] = row
                changed, row = imgui.input_float3(
                    ':Kernel R1', *GUI_STATE.kernelprop.data[1])
                print(f'R0 => CHANGED = {changed}, ROW = {row}')
                GUI_STATE.kernelprop.data[1] = row
                changed, row = imgui.input_float3(
                    ':Kernel R2', *GUI_STATE.kernelprop.data[2])
                print(f'R0 => CHANGED = {changed}, ROW = {row}')
                GUI_STATE.kernelprop.data[2] = row
            imgui.end()
