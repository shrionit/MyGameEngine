import glm


class Color(glm.vec4):
    def __init__(self, *args):
        args = list(args)
        if type(args[0]) == str:
            hx = args[0] if args[0][0] != '#' else args[0][1:]
            args = []
            for i in range(0, len(hx), 2):
                args.append(int(hx[i:i+2], 16))
        r = 4-len(args)
        if r != 0:
            for i in range(r):
                args += [1.0]
        args = [e/255 if type(e) == int else e for e in args]
        super().__init__(*args)


class Color3(glm.vec3):
    def __init__(self, *args):
        args = list(args)
        if type(args[0]) == str:
            hx = args[0] if args[0][0] != '#' else args[0][1:]
            args = []
            for i in range(0, len(hx), 2):
                args.append(int(hx[i:i+2], 16))
        r = 3-len(args)
        if r != 0:
            for i in range(r):
                args += [1.0]
        args = [e/255 if type(e) == int else e for e in args]
        super().__init__(*args)
