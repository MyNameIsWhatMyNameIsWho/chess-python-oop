from Move import Move
from Converters import enemy_color
from colorama import Fore


class Fig:
    letter = None
    key = None

    def __init__(self, color):
        self.color = color

    def __str__(self):
        res = ''
        if self.color == 1:
            res += Fore.LIGHTWHITE_EX
        else:
            res += Fore.BLACK
        return res + self.letter[self.color]

    def get_moves(self, y, x, board):
        return []

    def get_attacked_fields(self, y, x, board):
        moves = self.get_moves(y, x, board)
        fields = []
        for move in moves:
            fields.append((move.ty, move.tx))
        return fields


class Empty(Fig):
    def __init__(self):
        super().__init__(-1)

    def get_moves(self, y, x, board):
        raise Exception('Доступ к ходам без фигуры')

    def __str__(self):
        return ' '


class Knight(Fig):
    letter = ('n', 'N')
    key = 'N'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        moves = []
        directions = ((-2, -1), (-1, -2), (-2, 1), (1, -2), (2, -1), (-1, 2), (2, 1), (1, 2))
        for direction in directions:
            ny, nx = y + direction[0], x + direction[1]

            if board.is_empty_field(ny, nx):
                moves.append(Move(y, x, ny, nx, self.key, '-'))

            if board.get_fig(ny, nx, enemy_color(self.color)) is not None:
                moves.append(Move(y, x, ny, nx, self.key, 'x'))

        return moves


class Rook(Fig):
    letter = ('r', 'R')
    key = 'R'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        moves = []
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            ny, nx = y + direction[0], x + direction[1]
            while True:
                if board.is_empty_field(ny, nx):
                    moves.append(Move(y, x, ny, nx, self.key, '-'))
                elif board.get_fig(ny, nx, enemy_color(self.color)) is not None:
                    moves.append(Move(y, x, ny, nx, self.key, 'x'))
                    break
                else:
                    break
                ny, nx = ny + direction[0], nx + direction[1]
        return moves


class Bishop(Fig):
    letter = ('b', 'B')
    key = 'B'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        moves = []
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        for direction in directions:
            ny, nx = y + direction[0], x + direction[1]
            while True:
                if board.is_empty_field(ny, nx):
                    moves.append(Move(y, x, ny, nx, self.key, '-'))
                elif board.get_fig(ny, nx, enemy_color(self.color)) is not None:
                    moves.append(Move(y, x, ny, nx, self.key, 'x'))
                    break
                else:
                    break
                ny, nx = ny + direction[0], nx + direction[1]
        return moves


class Queen(Fig):
    letter = ('q', 'Q')
    key = 'Q'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        moves = []
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            ny, nx = y + direction[0], x + direction[1]
            while True:
                if board.is_empty_field(ny, nx):
                    moves.append(Move(y, x, ny, nx, self.key, '-'))
                elif board.get_fig(ny, nx, enemy_color(self.color)) is not None:
                    moves.append(Move(y, x, ny, nx, self.key, 'x'))
                    break
                else:
                    break
                ny, nx = ny + direction[0], nx + direction[1]
        return moves


class Pawn(Fig):
    letter = ('p', 'P')
    key = ''

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        moves = []
        # Для черной пешки
        if self.color == 0:
            # Обычный ход вперед
            if board.is_empty_field(y - 1, x):
                moves.append(Move(y, x, y - 1, x, self.key, '-'))
            # Длинный ход вперед
            if board.is_empty_field(y - 1, x) \
                    and board.is_empty_field(y - 2, x) \
                    and y == 6:
                moves.append(Move(y, x, y - 2, x, self.key, 'l'))

            # Взятия влево и вправо
            if board.get_fig(y - 1, x - 1, enemy_color(self.color)):
                moves.append(Move(y, x, y - 1, x - 1, self.key, 'x'))
            if board.get_fig(y - 1, x + 1, enemy_color(self.color)):
                moves.append(Move(y, x, y - 1, x + 1, self.key, 'x'))

            # Взятия на проходе
            if board.is_empty_field(y - 1, x - 1) and board.move_mask[y - 1][x - 1] == 2:
                moves.append(Move(y, x, y - 1, x - 1, self.key, 'xp'))
            if board.is_empty_field(y - 1, x + 1) and board.move_mask[y - 1][x + 1] == 2:
                moves.append(Move(y, x, y - 1, x + 1, self.key, 'xp'))

        # Для белой пешки
        if self.color == 1:
            # Обычный ход вперед
            if board.is_empty_field(y + 1, x):
                moves.append(Move(y, x, y + 1, x, self.key, '-'))
            # Длинный ход вперед
            if board.is_empty_field(y + 1, x) \
                    and board.is_empty_field(y + 2, x) \
                    and y == 1:
                moves.append(Move(y, x, y + 2, x, self.key, 'l'))

            # Взятия влево и вправо
            if board.get_fig(y + 1, x - 1, enemy_color(self.color)):
                moves.append(Move(y, x, y + 1, x - 1, self.key, 'x'))
            if board.get_fig(y + 1, x + 1, enemy_color(self.color)):
                moves.append(Move(y, x, y + 1, x + 1, self.key, 'x'))

            # Взятия на проходе
            if board.is_empty_field(y + 1, x - 1) and board.move_mask[y + 1][x - 1] == 2:
                moves.append(Move(y, x, y + 1, x - 1, self.key, 'xp'))
            if board.is_empty_field(y + 1, x + 1) and board.move_mask[y + 1][x + 1] == 2:
                moves.append(Move(y, x, y + 1, x + 1, self.key, 'xp'))
        return moves

    def get_attacked_fields(self, y, x, board):
        if self.color == 0:
            return [(y - 1, x - 1), (y - 1, x + 1)]
        else:
            return [(y + 1, x - 1), (y + 1, x + 1)]


class King(Fig):
    letter = ('k', 'K')
    key = 'K'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        moves = []
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            ny, nx = y + direction[0], x + direction[1]
            if board.is_empty_field(ny, nx):
                moves.append(Move(y, x, ny, nx, self.key, '-'))
            elif board.get_fig(ny, nx, enemy_color(self.color)) is not None:
                moves.append(Move(y, x, ny, nx, self.key, 'x'))

        # Рокировка в короткую сторону
        if board.is_empty_field(y, 5) and board.is_empty_field(y, 6)\
            and not board.is_attacked_field(y, 4, enemy_color(self.color)) \
            and not board.is_attacked_field(y, 5, enemy_color(self.color))\
            and not board.is_attacked_field(y, 6, enemy_color(self.color))\
            and board.move_mask[y][4] == 0 and board.move_mask[y][7] == 0:
            moves.append(Move(y, x, y, 6, self.key, '0-0'))
        # Рокировка в длинную сторону
        if board.is_empty_field(y, 1) and board.is_empty_field(y, 2) and board.is_empty_field(y, 3)\
                and not board.is_attacked_field(y, 2, enemy_color(self.color)) \
                and not board.is_attacked_field(y, 3, enemy_color(self.color)) \
                and not board.is_attacked_field(y, 4, enemy_color(self.color)) \
                and board.move_mask[y][4] == 0 and board.move_mask[y][0] == 0:
            moves.append(Move(y, x, y, 2, self.key, '0-0-0'))
        return moves

    def get_attacked_fields(self, y, x, board):
        fields = []
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            fields.append((y + direction[0], x + direction[1]))
        return fields


class Piece (Fig):
    letter = ('p', 'P')
    key = 'p'

    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, y, x, board):
        moves = []
        directions = ((-1 + 2 * self.color, -1), (-1 + 2 * self.color, 1))

        for direction in directions:
            if board.get_fig(direction[0] + y, direction[1] + x, color=enemy_color(self.color)) is not None and \
                    board.is_empty_field(2 * direction[0] + y, 2 * direction[1] + x):
                moves.append(Move(y, x, 2 * direction[0] + y, 2 * direction[1] + x, self.key, 'x',\
                                  extra_info='K' if 2 * direction[0] + y == self.color * 7 else None))

            if board.is_empty_field(direction[0] + y, direction[1] + x):
                moves.append(Move(y, x, direction[0] + y, direction[1] + x, self.key, '-',\
                                  extra_info='K' if direction[0] + y == self.color * 7 else None))

        return moves

    def get_attacked_fields(self, y, x, board):
        fields = []
        for move in self.get_moves(y, x, board):
            if move.mode == 'x':
                fields.append(((move.ty + move.fy) / 2, (move.tx + move.fx) / 2))
        return fields



class PieceKing (Fig):
    letter = ('k', 'K')
    key = 'k'

    def __init__(self, color):
        super().__init__(color)

    def __stopper(self, ny, nx, board, eat):
        if eat:
            return board.is_empty_field(ny, nx)
        else:
            return board.get_fig(ny, nx, color=self.color) is None and 0 <= ny <= 7 and 0 <= nx <= 7

    def get_moves(self, y, x, board):
        moves = []
        directions = (
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        )
        for direction in directions:
            ny, nx = y + direction[0], x + direction[1]
            eat = False
            while self.__stopper(ny, nx, board, eat):
                if eat:
                    moves.append(Move(y, x, ny, nx, self.key, 'x'))
                else:
                    if board.is_empty_field(ny, nx):
                        moves.append(Move(y, x, ny, nx, self.key, '-'))
                    elif board.get_fig(ny, nx, color=enemy_color(self.color)) is not None:
                        eat = True
                ny += direction[0]
                nx += direction[1]
        return moves


class QK (Queen, Knight):
    letter = ('d', 'D')
    key = 'd'

    def __init__(self, color):
        Queen.__init__(self, color)
        Knight.__init__(self, color)

    def get_moves(self, y, x, board):
        return Queen.get_moves(self, y, x, board) + Knight.get_moves(self, y, x, board)

    def get_attacked_fields(self, y, x, board):
        return Queen.get_attacked_fields(self, y, x, board) + Knight.get_attacked_fields(self, y, x, board)


class RK (Rook, Knight):
    letter = ('a', 'A')
    key = 'a'

    def __init__(self, color):
        Rook.__init__(self, color)
        Knight.__init__(self, color)

    def get_moves(self, y, x, board):
        return Rook.get_moves(self, y, x, board) + Knight.get_moves(self, y, x, board)

    def get_attacked_fields(self, y, x, board):
        return Rook.get_attacked_fields(self, y, x, board) + Knight.get_attacked_fields(self, y, x, board)


class BK (Bishop, Knight):
    letter = ('s', 'S')
    key = 's'

    def __init__(self, color):
        Bishop.__init__(self, color)
        Knight.__init__(self, color)

    def get_moves(self, y, x, board):
        return Bishop.get_moves(self, y, x, board) + Knight.get_moves(self, y, x, board)

    def get_attacked_fields(self, y, x, board):
        return Bishop.get_attacked_fields(self, y, x, board) + Knight.get_attacked_fields(self, y, x, board)
