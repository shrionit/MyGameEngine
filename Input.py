import glfw as g

mouse = {'x': 0, 'y': 0}


def getmouse(w):
    mx, my = g.get_cursor_pos(w)
    width, height = g.get_window_size(w)
    if(mx > 0 and mx < width and my > 0 and my < height):
        flag = True
        mouse = {'x': mx, 'y': my}


def onscroll(w, f):
    if flag:
        g.set_scroll_callback(w, f)
