import logging
import webcolors
import numpy
from anytree import Node, RenderTree, find_by_attr

logger = logging.Logger('catch_all')
tokens = []

final_code = []
last_commands = []
tree = "Parent Child"
tree_last = ""

grammars = ["mov", "mo", "m", "loo", "lo", "l", "las", "la", "animatio", "animati", "animat", "anima", "anim", "ani",
            "an", "a", "colo", "col", "c", "co", "dow", "do", "d", "righ", "rig", "ri", "r", "lef", "le", "i"]


# print(code + "-" * 20)


def lexer(plain_code):
    tok = ""
    temp_number = ""
    temp_color = ""
    temp_times = ""
    open_br = False
    set_color = False
    loop = False

    global tokens

    plain_code = list(plain_code)
    print(plain_code)

    for char in plain_code:
        tok += char
        if tok == " ":
            tok = ""

        elif tok.lower() == "if":
            tokens.append("IF")
            tok = ""

        elif tok == "<":
            tokens.append("OPEN_IF_BRACKET")
            # loop = True
            tok = ""
        elif tok == ">":
            tokens.append("CLOSE_IF_BRACKET")
            # loop = False
            tok = ""

        elif tok.lower() == "loop":
            tokens.append("LOOP")
            tok = ""

        elif tok == "{":
            tokens.append("OPEN_LOOP_BRACKET")
            loop = True
            tok = ""
        elif tok == "}":
            tokens.append("TIMES:" + temp_times)
            tokens.append("CLOSE_LOOP_BRACKET")
            loop = False
            temp_times = ""
            tok = ""

        elif loop:
            if tok in "1234567890":
                temp_times += char
            else:
                tokens = ["Error!"]
                return tokens
            tok = ""

        elif tok.lower() == "move":
            tokens.append("MOVE")
            tok = ""
        elif tok.lower() == "last":
            tokens.append("LAST")
            tok = ""
        elif tok.lower() == "animation":
            tokens.append("ANIMATION")
            tok = ""
        elif tok.lower() == "color":
            tokens.append("COLOR")
            tok = ""

        elif tok == "[":
            tokens.append("OPEN_SQ_BRACKET")
            set_color = True
            tok = ""
        elif tok == "]":
            if len(temp_color) != 7:
                tokens = ["Error!"]
                return tokens
            tokens.append("CODE:" + temp_color)
            tokens.append("CLOSE_SQ_BRACKET")
            set_color = False
            temp_color = ""
            tok = ""

        elif set_color:
            if tok in "1234567890abcdefABCDEF#":
                temp_color += char
            else:
                tokens = ["Error!"]
                return tokens
            tok = ""

        elif tok == ".":
            tokens.append("DOT")
            tok = ""
        elif tok.lower() == "up":
            tokens.append("UP")
            tok = ""
        elif tok.lower() == "down":
            tokens.append("DOWN")
            tok = ""
        elif tok.lower() == "right":
            tokens.append("RIGHT")
            tok = ""
        elif tok.lower() == "left":
            tokens.append("LEFT")
            tok = ""
        elif tok == "(":
            tokens.append("OPEN_BRACKET")
            open_br = True
            tok = ""
        elif tok == ")":
            """print(temp_number)
            print("FOUND CLOSE_BRACKET")"""
            tokens.append("NUMBER:" + temp_number)
            tokens.append("CLOSE_BRACKET")
            open_br = False
            temp_number = ""
            tok = ""

        elif open_br:
            if tok in "1234567890":
                temp_number += char
            else:
                tokens = ["Error!"]
                return tokens
            tok = ""

        elif tok == "\n":
            tok = ""
        elif tok not in "move.updownrightleft(0987654321)lastanimationcolour[]#{}loopif<>":
            tokens = ["Error!"]
            return tokens

    print(tokens)
    return tokens


def parser_old(toks):
    if toks[0] == "Error!":
        print(toks[0])
        return

    i = 0
    global tree
    global tree_last
    global final_code
    global last_commands
    command_list = []

    looping = False
    loop_times = 0

    tree_id = 1



    for a in range(len(toks) - 1):
        if a < len(toks) - 1:
            if toks[a] == toks[a + 1]:
                raise ValueError('Repeated code.')

    while i < len(toks) - 1:
        if toks[i] + " " + toks[i + 1] == "MOVE DOT":
            command_list.append("move")
            tree += "\nroot move.{}".format(tree_id)
            # print("FOUND ENTRY")
            current_dir = ""
            current_num = ""
            if toks[i + 2] == "UP":
                # print("FOUND UP")
                command_list.append("up")
                if looping:
                    tree += "loop.{} move.{}\nmove.{} up".format(tree_id, tree_id, tree_id)
                else:
                    tree += "\nmove.{} up".format(tree_id)
                current_dir = "up"
                i += 1
            elif toks[i + 2] == "DOWN":
                # print("FOUND DOWN")
                command_list.append("down")
                tree += "\nmove.{} down".format(tree_id)
                current_dir = "down"
                i += 1
            elif toks[i + 2] == "RIGHT":
                # print("FOUND RIGHT")
                command_list.append("right")
                tree += "\nmove.{} right".format(tree_id)
                current_dir = "right"
                i += 1
            elif toks[i + 2] == "LEFT":
                # print("FOUND LEFT")
                command_list.append("left")
                tree += "\nmove.{} left".format(tree_id)
                current_dir = "left"
                i += 1
            if toks[i + 3][0:7] == "NUMBER:":
                number = toks[i + 3][7:]
                current_num = number
                if number == "":
                    raise ValueError('Not complete code.')
                command_list.append(number)
                if looping:
                    number = str(int(number) * loop_times) + "_with_loop"
                    current_num = number

                tree += "\n{} {}".format(current_dir, current_num)
                i += 2
            if i + 6 < len(toks) - 1:
                if toks[i + 3] + " " + toks[i + 4] == "DOT ANIMATION":
                    if toks[i + 6][0:7] == "NUMBER:":
                        number = toks[i + 6][7:]
                        if number == "":
                            raise ValueError('Not complete code.')
                        command_list.append(number)

                        tree += "\n{} animation\nanimation {}".format(current_num, number)
                    try:
                        if toks[i + 8] == "DOT":
                            raise ValueError('Not complete code.')
                    except IndexError:
                        pass
            i += 2
            # print(command_list)
            final_code.append(build_command(command_list))
            command_list = []
            looping = False
            tree_id += 1

        elif i + 3 < len(toks) - 1:
            if toks[i] + " " + toks[i + 1] + " " + toks[i + 2] + " " + toks[i + 3] == "LAST DOT MOVE DOT":
                command_list.append("move")
                tree_last += "\nlast move.{}".format(tree_id)
                # print("FOUND ENTRY")
                current_dir = ""
                current_num = ""
                if toks[i + 4] == "UP":
                    # print("FOUND UP")
                    command_list.append("up")
                    tree_last += "\nmove.{} up".format(tree_id)
                    current_dir = "up"
                    i += 1
                elif toks[i + 4] == "DOWN":
                    # print("FOUND DOWN")
                    command_list.append("down")
                    tree_last += "\nmove.{} down".format(tree_id)
                    current_dir = "down"
                    i += 1
                elif toks[i + 4] == "RIGHT":
                    # print("FOUND RIGHT")
                    command_list.append("right")
                    tree_last += "\nmove.{} right".format(tree_id)
                    current_dir = "right"
                    i += 1
                elif toks[i + 4] == "LEFT":
                    # print("FOUND LEFT")
                    command_list.append("left")
                    tree_last += "\nmove.{} left".format(tree_id)
                    current_dir = "left"
                    i += 1
                if toks[i + 5][0:7] == "NUMBER:":
                    number = toks[i + 5][7:]
                    current_num = number
                    if number == "":
                        raise ValueError('Not complete code.')
                    command_list.append(number)
                    if looping:
                        number = str(int(number) * loop_times) + "_with_loop"
                        current_num = number
                    tree_last += "\n{} {}".format(current_dir, current_num)
                    i += 2
                if i + 8 < len(toks) - 1:
                    if toks[i + 5] + " " + toks[i + 6] == "DOT ANIMATION":
                        if toks[i + 8][0:7] == "NUMBER:":
                            number = toks[i + 8][7:]
                            if number == "":
                                raise ValueError('Not complete code.')
                            command_list.append(number)
                            tree_last += "\n{} animation\nanimation {}".format(current_num, number)
                    try:
                        if toks[i + 10] == "DOT":
                            raise ValueError('Not complete code.')
                    except IndexError:
                        pass
                i += 4

                last_commands.append(build_command(command_list))
                command_list = []
                looping = False
                tree_id += 1

        if i + 3 < len(toks) - 1:
            if toks[i] + " " + toks[i + 1] + " " + toks[i + 2][0:5] == "LOOP OPEN_LOOP_BRACKET TIMES":
                if looping:
                    raise ValueError('Not complete code.')
                try:
                    if toks[i - 2] == "LAST":
                        raise ValueError('Not complete code.')
                except IndexError:
                    pass
                number = toks[i + 2][6:]
                if number == "":
                    raise ValueError('Not complete code.')
                command_list.append("loop")
                command_list.append(number)

                try:
                    if toks[i + 5] == "LAST":
                        raise ValueError('Not complete code.')
                except IndexError:
                    pass
                i += 3

                looping = True
                loop_times = int(number)

        if i + 10 < len(toks) - 1:
            if toks[i] + " " + toks[i + 1] + " " + toks[i + 2] + " " + toks[i + 3] + " " + toks[i + 4][
                                                                                           0:4] == "IF OPEN_IF_BRACKET COLOR OPEN_SQ_BRACKET CODE":
                if toks[i + 7] + " " + toks[i + 8] + " " + toks[i + 9] + " " + toks[i + 10][
                                                                               0:4] != "DOT COLOR OPEN_SQ_BRACKET CODE":
                    raise ValueError('Not complete code.')
                try:
                    if toks[i - 2] == "LAST":
                        raise ValueError('Not complete code.')
                except IndexError:
                    pass

                color_check = toks[i + 4][6:]
                color_set = toks[i + 10][6:]

                tree += "\tif\n\t\tcolor\n\t\t\t #" + color_check + "\n\t\t\t\t    than\n\t\t\t\t\t    #" + color_set + "\n"

                command_list.append("if")
                command_list.append(color_check)
                command_list.append(color_set)
                final_code.append(build_command(command_list))
                command_list = []

                i += 10

        if i + 4 < len(toks) - 1:
            if toks[i] + " " + toks[i + 1] + " " + toks[i + 2] + " " + toks[i + 3] + " " + toks[i + 4][
                                                                                           0:4] == "LAST DOT COLOR OPEN_SQ_BRACKET CODE":
                try:
                    if toks[i + 6] == "DOT":
                        raise ValueError('Not complete code.')
                except IndexError:
                    pass
                color = toks[i + 4][6:]
                command_list.append(color)
                last_commands.append(build_command(command_list))
                command_list = []

                tree_last += "\nlast color.{}\ncolor.{} #{}".format(tree_id, tree_id, color)
                i += 5
                tree_id += 1

        if i + 2 < len(toks) - 1:
            if toks[i] + " " + toks[i + 1] + " " + toks[i + 2][0:4] == "COLOR OPEN_SQ_BRACKET CODE":
                if i + 4 < len(toks) - 1:
                    if toks[i + 4] == "DOT":
                        raise ValueError('Not complete code.')
                color = toks[i + 2][6:]
                command_list.append(color)
                final_code.append(build_command(command_list))
                command_list = []
                tree += "\nroot color.{}\ncolor.{} #{}".format(tree_id, tree_id, color)
                i += 3
                tree_id += 1

        if toks[len(toks) - 1] == "DOT" or toks[len(toks) - 1] == "ANIMATION":
            raise ValueError('Not complete code.')
        i += 1
    tree += "\nroot last"

def parser(toks):
    if toks[0] == "Error!":
        raise ValueError("Something bad in parser!")

    global tree
    global tree_last
    global final_code
    global last_commands

    command_list = []

    looping = False

    main_range = len(toks) - 1
    loop_times = 0
    tree_id = 1
    i = 0

    for a in range(main_range):
        if a < main_range:
            if toks[a] == toks[a + 1]:
                raise ValueError('Repeated code!')

    while i < main_range:
        if toks[i] == "MOVE":
            if toks[i + 1] != "DOT":
                raise ValueError('Bad code!')

            current_dir = ""
            current_num = ""

            command_list.append("move")
            tree += "\nroot move.{}".format(tree_id)

            if toks[i + 2] == "UP":
                current_dir = "up"

                command_list.append("up")
                if looping:
                    tree += "loop.{} move.{}\nmove.{} up".format(tree_id, tree_id, tree_id)
                else:
                    tree += "\nmove.{} up".format(tree_id)
                i += 1
            elif toks[i + 2] == "DOWN":
                current_dir = "down"

                command_list.append("down")
                tree += "\nmove.{} down".format(tree_id)
                i += 1
            elif toks[i + 2] == "RIGHT":
                current_dir = "right"

                command_list.append("right")
                tree += "\nmove.{} right".format(tree_id)
                i += 1
            elif toks[i + 2] == "LEFT":
                current_dir = "left"

                command_list.append("left")
                tree += "\nmove.{} left".format(tree_id)
                i += 1
            else:
                raise ValueError('Bad code!')

            if toks[i + 3][0:7] != "NUMBER:":
                raise ValueError('Bad code!')

            number = toks[i + 3][7:]
            current_num = number
            if number == "":
                raise ValueError('Missing number!')
            command_list.append(number)
            if looping:
                number = str(int(number) * loop_times) + "_with_loop"
                current_num = number

            tree += "\n{} {}".format(current_dir, current_num)
            i += 2

            try:
                if toks[i + 3] + " " + toks[i + 4] == "DOT ANIMATION":
                    if toks[i + 6][0:7] != "NUMBER:":
                        raise ValueError('Bad code!')

                    number = toks[i + 6][7:]
                    if number == "":
                        raise ValueError('Missing number!')

                    command_list.append(number)
                    tree += "\n{} animation\nanimation {}".format(current_num, number)

                    try:
                        if toks[i + 8] == "DOT":
                            raise ValueError('Bad code!')
                    except IndexError:
                        pass
            except IndexError:
                pass

            print(command_list)
            final_code.append(build_command(command_list))

            command_list = []
            looping = False
            tree_id += 1
            i += 2

def build_command(element_list):
    string = ""
    animation = "in_out_cubic"
    if len(element_list) == 4:
        if element_list[3] == "1":
            animation = "in_out_back"
        elif element_list[3] == "2":
            animation = "in_out_bounce"
        elif element_list[3] == "3":
            animation = "in_out_circ"
        elif element_list[3] == "4":
            animation = "in_expo"
        elif element_list[3] == "5":
            animation = "in_quint"
        elif element_list[3] == "6":
            animation = "linear"
        elif element_list[3] == "7":
            animation = "out_sine"
        elif element_list[3] == "8":
            animation = "out_quad"
        elif element_list[3] == "9":
            animation = "out_cubic"
        else:
            raise ValueError('Not complete code.')

    # move_up(self, 2, timer())
    if element_list[0] == "move":
        string += element_list[0] + "_" + element_list[1] + "(self, " + element_list[2] + ", timer(), '" \
                  + animation + "') "

    elif element_list[0] == "loop":
        string += "for i in range(" + element_list[1] + "):"
        string += "\n\t\t" + element_list[2] + "_" + element_list[3] + "(self, " + element_list[4] + ", timer(), '" \
                  + animation + "') "

        #	if get_color(self) != 'ffffff':
        #	    setcolor
    elif element_list[0] == "if":
        color_code_check = "#" + element_list[1]
        color_to_change = "#" + element_list[2]
        # string += "timer()"
        string += "if get_color(self, timer()) == " + str(
            tuple(numpy.array(webcolors.hex_to_rgb(color_code_check)) / 255.0)) + ":"
        color = tuple(numpy.array(webcolors.hex_to_rgb(color_to_change)) / 255.0)
        # string += "\n\t\ttimer()"
        string += "\n\t\tchange_color(self, " + str(color) + ", timer())"
        string += "\n\t\tprint('Changed', '-'*100)"
        # string += "\n\ttimer()"

    # change_color(self, color)
    else:
        color_code = "#" + element_list[0]
        color = tuple(numpy.array(webcolors.hex_to_rgb(color_code)) / 255.0)
        string += "change_color(self, " + str(color) + ", timer())"

    return string


def run(input_code):
    global final_code, last_commands, tree
    errors = False

    toks = lexer(input_code)

    try:
        parser(toks)
    except BaseException as e:
        logger.error("Something wrong!")
        errors = True

    data = [final_code + last_commands, tree + tree_last, errors]
    print(data)
    return data


def run_test(input_code):
    global final_code, last_commands, tree
    errors = False

    toks = lexer(input_code)
    parser(toks)

    data = [final_code + last_commands, tree + tree_last, errors]
    #print(data)
    #print(tree + tree_last)

    f = open("tree_text.txt", "w+")
    f.write(tree + tree_last)
    f.close()

    with open('tree_text.txt', 'r') as f:
        lines = f.readlines()[1:]
        root = Node(lines[0].split(" ")[0])
        nodes = {}
        nodes[root.name] = root

        for line in lines:
            line = line.split(" ")
            name = "".join(line[1:]).strip()
            nodes[name] = Node(name, parent=nodes[line[0]])

        for pre, _, node in RenderTree(root):
            print("%s%s" % (pre, node.name))





code = """move.up(2))
"""

run_test(code)
