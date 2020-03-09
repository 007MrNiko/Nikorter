import logging
import webcolors
import numpy

logger = logging.Logger('catch_all')
tokens = []

final_code = []
last_commands = []
tree = "PROGRAM TREE:\n"
tree_last = ""


# print(code + "-" * 20)


def lexer(plain_code):
    tok = ""
    temp_number = ""
    temp_color = ""
    open_br = False
    set_color = False

    global tokens

    plain_code = list(plain_code)
    print(plain_code)

    for char in plain_code:
        tok += char
        if tok == " ":
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
        elif tok.lower() == "color" or tok.lower() == "colour":
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
        else:
            if tok not in "move.updownrightleft(0987654321)lastanimationcolour[]#":
                tokens = ["Error!"]
                return tokens

    print(tokens)
    return tokens


def parser(toks):
    if toks[0] == "Error!":
        print(toks[0])
        return

    i = 0
    global tree
    global tree_last
    global final_code
    global last_commands
    command_list = []
    while i < len(toks) - 1:
        if toks[i] + " " + toks[i + 1] == "MOVE DOT":
            command_list.append("move")
            tree += "move\n"
            # print("FOUND ENTRY")
            if toks[i + 2] == "UP":
                # print("FOUND UP")
                command_list.append("up")
                tree += "\tup\n"
                i += 1
            elif toks[i + 2] == "DOWN":
                # print("FOUND DOWN")
                command_list.append("down")
                tree += "\tdown\n"
                i += 1
            elif toks[i + 2] == "RIGHT":
                # print("FOUND RIGHT")
                command_list.append("right")
                tree += "\tright\n"
                i += 1
            elif toks[i + 2] == "LEFT":
                # print("FOUND LEFT")
                command_list.append("left")
                tree += "\tleft\n"
                i += 1
            if toks[i + 3][0:7] == "NUMBER:":
                number = toks[i + 3][7:]
                if number == "":
                    raise ValueError('Not complete code.')
                command_list.append(number)
                tree += "\t\t{}\n".format(number)
                i += 2
            if i + 6 < len(toks) - 1:
                if toks[i + 3] + " " + toks[i + 4] == "DOT ANIMATION":
                    if toks[i + 6][0:7] == "NUMBER:":
                        number = toks[i + 6][7:]
                        if number == "":
                            raise ValueError('Not complete code.')
                        command_list.append(number)
                        tree += "\t\t  animation\n\t\t\t\t    {}\n".format(number)
                    if toks[i+8] == "DOT":
                        raise ValueError('Not complete code.')
            i += 2
            # print(command_list)
            final_code.append(build_command(command_list))
            command_list = []

        elif i + 3 < len(toks) - 1:
            if toks[i] + " " + toks[i + 1] + " " + toks[i + 2] + " " + toks[i + 3] == "LAST DOT MOVE DOT":
                command_list.append("move")
                tree_last += "last\n"
                tree_last += "\tmove\n"
                # print("FOUND ENTRY")
                if toks[i + 4] == "UP":
                    # print("FOUND UP")
                    command_list.append("up")
                    tree_last += "\t\tup\n"
                    i += 1
                elif toks[i + 4] == "DOWN":
                    # print("FOUND DOWN")
                    command_list.append("down")
                    tree_last += "\t\tdown\n"
                    i += 1
                elif toks[i + 4] == "RIGHT":
                    # print("FOUND RIGHT")
                    command_list.append("right")
                    tree_last += "\t\tright\n"
                    i += 1
                elif toks[i + 4] == "LEFT":
                    # print("FOUND LEFT")
                    command_list.append("left")
                    tree_last += "\t\tleft\n"
                    i += 1
                if toks[i + 5][0:7] == "NUMBER:":
                    number = toks[i + 5][7:]
                    if number == "":
                        raise ValueError('Not complete code.')
                    command_list.append(number)
                    tree_last += "\t\t\t{}\n".format(number)
                    i += 2
                if i + 8 < len(toks) - 1:
                    if toks[i + 5] + " " + toks[i + 6] == "DOT ANIMATION":
                        if toks[i + 8][0:7] == "NUMBER:":
                            number = toks[i + 8][7:]
                            if number == "":
                                raise ValueError('Not complete code.')
                            command_list.append(number)
                            tree_last += "\t\t\t  animation\n\t\t\t\t\t    {}\n".format(number)
                    try:
                        if toks[i+10] == "DOT":
                            raise ValueError('Not complete code.')
                    except IndexError:
                        pass
                i += 4

                last_commands.append(build_command(command_list))
                command_list = []

        if i + 2 < len(toks) - 1:
            if toks[i] + " " + toks[i + 1] + " " + toks[i + 2][0:4] == "COLOR OPEN_SQ_BRACKET CODE":
                if i + 4 < len(toks) - 1:
                    if toks[i + 4] == "DOT":
                        raise ValueError('Not complete code.')
                color = toks[i + 2][6:]
                command_list.append(color)
                final_code.append(build_command(command_list))
                command_list = []
                tree += "color\n\t" + color + "\n"
                i += 3

        if i + 6 < len(toks) - 1:
            if toks[i] + " " + toks[i + 1] + " " + toks[i + 2] + " " + toks[i + 3] + " " + toks[i + 4][0:4] == "LAST DOT COLOR OPEN_SQ_BRACKET CODE":
                if i + 6 < len(toks) - 1:
                    if toks[i + 6] == "DOT":
                        raise ValueError('Not complete code.')
                color = toks[i + 4][6:]
                command_list.append(color)
                last_commands.append(build_command(command_list))
                command_list = []
                tree_last += "last\n\tcolor\n\t\t" + color + "\n"
                i += 5

        if toks[len(toks) - 1] == "DOT" or toks[len(toks) - 1] == "ANIMATION":
            raise ValueError('Not complete code.')
        i += 1


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
    print(data)
    print(last_commands)
    return data


code = """last.color[#ff0000]
color[#0000ff]
move.up(2)
color[#00ff00]
move.right(4).animation(2)
last.move.up(2).animation(3)
"""

# run_test(code)
