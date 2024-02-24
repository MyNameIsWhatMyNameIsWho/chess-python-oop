def m2c(coords):
    y = int(coords[1]) - 1
    x = ord(coords[0]) - ord('A')
    return y, x


def c2m(y, x):
    pos = ''
    y = 1 + y
    pos += ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'][x]
    pos += str(y)
    return pos


def t2m(t):
    mode_dict = {
        '-': '-',
        'x': 'x',
        'l': '-',
        'xp': 'x'
    }
    if t in mode_dict.keys():
        return mode_dict[t]
    else:
        raise Exception('Неизвестный тип хода')


def enemy_color(color):
    return (color + 1) % 2
