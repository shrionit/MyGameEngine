from abc import ABCMeta, abstractmethod

import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
from glm import *
from model.texture import Texture
import numpy as np
from PIL import Image
from shader import Shader
from .color import *


class O(object):
    pass


class DProp(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError('No such attribute: ' + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError('No such attribute: '+name)


class GUI(GlfwRenderer, metaclass=ABCMeta):
    """     GUI Only For GLFW WINDOWS.
        This class has static kind variable to attach to a glfw window
        To set WINDOW:
                GUI.WINDOW = glfwwindow_object
        To set default FONT:
                GUI.FONT = 'font_file_name.ttf'
        To set SCALE FACTOR of SIZE:
                GUI.SCALE_FACTOR = N default is 2
        To set default FONT SIZE:
                GUI.FONT_SIZE = 'font_file_name.ttf'
    """
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
        self.GUI_STATE = None
        self.SHADER = None
        self.props = DProp({
            'steps': 0.100,
            'mode': 1,
            'active': True
        })
        # GUI_STATE.renderprop.img = framebufferid if framebufferid != 0 else Texture(
        #     Image.new('RGBA', (512, 512), 'BLACK'), isimg=True).getTexID()
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

    def gengui(self, props: dict):
        self.GUI_STATE = DProp(props)
        print('GENGUI = ', self.GUI_STATE.renderprop)

    def giveshader(self, shaders: DProp):
        self.SHADER = shaders

    def newframe(self, id):
        self.GUI_STATE.renderprop.img = id

    def getdata(self, data, o=False, dtype='f'):
        return np.array([e for e in data.split() if e != '-'], dtype=np.float32)

    def draw(self):
        if self.GUI_STATE:
            with imgui.font(self.new_font):
                imgui.begin("Test")
                imgui.set_scroll_here()
                self.vanilla_view_props()
                self.kernel_props()
                self.light_props()
                imgui.end()

    def vanilla_view_props(self):
        # Vanilla Render View
        expanded0, visible = imgui.collapsing_header(
            'Raw Scene', self.GUI_STATE.renderprop.isvisible)
        if expanded0:
            imgui.image(self.GUI_STATE.renderprop.img, 256, 256, (0, 1),
                        (1, 0), border_color=(0.5, 0.3, 0.2, 1.0))
            changed, self.GUI_STATE.renderprop.gamma = imgui.input_float(
                ' : Gamma', self.GUI_STATE.renderprop.gamma)
            # self.SHADER.frame_shader.attach()
            self.SHADER.frame_shader.putDataInUniformLocation(
                'gamma', self.GUI_STATE.renderprop.gamma)
            # self.SHADER.frame_shader.detach()

    def kernel_props(self):
        # Kernel Matrix
        expanded1, visible = imgui.collapsing_header(
            'Kernel', self.GUI_STATE.kernelprop.isvisible)
        if expanded1:
            changed0, row = imgui.input_float3(
                ':Kernel R0', *self.GUI_STATE.kernelprop.row[0])
            if changed0:
                self.GUI_STATE.kernelprop.row[0] = row
                for i in range(3):
                    self.SHADER.frame_shader.putDataInUniformLocation(
                        f'kernel[{i}]', self.GUI_STATE.kernelprop.row[0][i])
                self.SHADER.frame_shader.detach()

            changed1, row = imgui.input_float3(
                ':Kernel R1', *self.GUI_STATE.kernelprop.row[1])
            if changed1:
                self.GUI_STATE.kernelprop.row[1] = row
                for i in range(3):
                    print(self.GUI_STATE.kernelprop.row[1][i])
                    self.SHADER.frame_shader.putDataInUniformLocation(
                        f'kernel[{i+3}]',
                        self.GUI_STATE.kernelprop.row[1][i]
                    )

            changed2, row = imgui.input_float3(
                ':Kernel R2', *self.GUI_STATE.kernelprop.row[2])
            if changed2:
                self.GUI_STATE.kernelprop.row[2] = row
                for i in range(3):
                    self.SHADER.frame_shader.putDataInUniformLocation(
                        f'kernel[{i+6}]', self.GUI_STATE.kernelprop.row[2][i])

    def light_props(self):
        expanded, visible = imgui.collapsing_header(
            'Lighting', self.GUI_STATE.lightprop.isvisible)
        style = imgui.get_style()
        if expanded:
            self.SHADER.scene_shader.attach()
            imgui.columns(2, 'GHOST')
            w = imgui.get_window_width()
            imgui.set_column_width(0, w*0.6)
            changed, self.GUI_STATE.lightprop.shininess = imgui.drag_float(
                'Shininess', self.GUI_STATE.lightprop.shininess, self.props.steps, 0.001, 30.0)
            if changed:
                self.SHADER.scene_shader.putDataInUniformLocation(
                    'shininess', self.GUI_STATE.lightprop.shininess)
            imgui.next_column()
            imgui.set_column_width(1, w*0.4)
            changed, self.props.steps = imgui.input_float(
                'Step',
                self.props.steps
            )
            imgui.columns(1)
            changed0, self.GUI_STATE.lightprop.specDamp = imgui.drag_float(
                'Specular Damp', self.GUI_STATE.lightprop.specDamp, self.props.steps, 0.001, 30.0)
            if changed0:
                self.SHADER.scene_shader.putDataInUniformLocation(
                    'specDamp',
                    self.GUI_STATE.lightprop.specDamp
                )
            changed1, self.GUI_STATE.lightprop.lightcolor = imgui.color_edit3(
                'Light Color', *self.GUI_STATE.lightprop.lightcolor
            )
            self.GUI_STATE.lightprop.lightcolor = Color3(
                *self.GUI_STATE.lightprop.lightcolor)
            if changed1:
                self.SHADER.scene_shader.putDataInUniformLocation(
                    'lightColor',
                    self.GUI_STATE.lightprop.lightcolor
                )
            if imgui.radio_button('BLINN', self.props.active):
                self.props.active = not self.props.active
            if self.props.active:
                self.SHADER.scene_shader.putDataInUniformLocation(
                    'blinn',
                    1,
                    dtype='i'
                )
            else:
                self.SHADER.scene_shader.putDataInUniformLocation(
                    'blinn',
                    0,
                    dtype='i'
                )
            # self.SHADER.scene_shader.detach()
