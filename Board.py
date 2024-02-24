from Fig import Empty, Knight, Rook, Bishop, Queen, Pawn, King, QK, RK, BK
from Converters import enemy_color
from colorama import Back, Style


class Board:
    def __init__(self):
        self.moves = []
        self.board = []
        self.move_mask = []
        self._generate_new_field()

    def _generate_new_field(self):
        self.moves = []
        self.board = [
            [Rook(1), Knight(1), Bishop(1), Queen(1), King(1), Bishop(1), Knight(1), Rook(1)],
            [Pawn(1) for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Pawn(0) for x in range(8)],
            [Rook(0), Knight(0), Bishop(0), Queen(0), King(0), Bishop(0), Knight(0), Rook(0)]
        ]
        self.move_mask = [[0 for x in range(8)] for y in range(8)]

    def show(self, for_player, moves=None):
        if moves is None:
            moves = []
        fields = []
        for move in moves:
            fields.append((move.ty, move.tx))
        res = ''
        res += '    A B C D E F G H  \n' if for_player == 1 else '    H G F E D C B A \n'
        res += '\n'
        for y in (range(8) if for_player == 0 else range(7, -1, -1)):
            res += f'{y + 1}   '
            for x in (range(8) if for_player == 1 else range(7, -1, -1)):
                if (y, x) in fields:
                    res += Back.GREEN
                elif (y + x) % 2 == 0:
                    res += Back.LIGHTBLACK_EX
                else:
                    res += Back.WHITE

                res += str(self.board[y][x])
                res += ' ' + Style.RESET_ALL

            res += f'   {y + 1}\n'

        res += '\n'
        res += '    A B C D E F G H  \n' if for_player == 1 else '    H G F E D C B A \n'
        return res

    def danger(self, for_player):
        moves = []
        for y in range(8):
            for x in range(8):
                cur_moves = self.get_val_moves(y, x, enemy_color(for_player))
                for move in cur_moves:
                    if move.mode == 'x':
                        moves.append(move)
        res = self.show(for_player, moves)
        if self.check_for_shah(for_player):
            res += 'Шах!'
        return res

    def get_fig(self, y, x, color=None):
        if color is None:
            if 0 <= y <= 7 and 0 <= x <= 7:
                return self.board[y][x]
            else:
                return None
        else:
            fig = self.get_fig(y, x)
            if fig is not None and fig.color == color:
                return fig
            else:
                return None

    def is_empty_field(self, y, x):
        return self.get_fig(y, x, -1) is not None

    def get_moves(self, y, x, color):
        # print(y, x)
        fig = self.get_fig(y, x, color)
        if fig is None:
            return []
        else:
            # print(list(map(str, fig.get_moves(y, x, self))))
            return fig.get_moves(y, x, self)

    def perform_move(self, move):
        fy, fx, ty, tx = move()
        self.board[ty][tx] = self.board[fy][fx]
        self.board[fy][fx] = Empty()
        self.__update_move_mask(move)

        if move.mode == 'xp':
            self.board[fy][tx] = Empty()

        if move.mode == '0-0':
            self.board[fy][5] = self.board[fy][7]
            self.board[fy][7] = Empty()

        if move.mode == '0-0-0':
            self.board[fy][5] = self.board[fy][7]
            self.board[fy][7] = Empty()

        self.moves.append(move)
        if move.key == '' and ty in (0, 7) and move.extra_info is None:
            return 'pawn'
        if move.key == '' and ty in (0, 7) and move.extra_info is not None:
            figs = {'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight}
            color = 0 if ty == 0 else 1
            self.board[ty][tx] = figs[move.extra_info](color)

        return None

    def __update_move_mask(self, move):
        fy, fx, ty, tx = move()
        self.move_mask[fy][fx] = 1
        self.move_mask[ty][tx] = 1
        for y in range(8):
            for x in range(8):
                if self.move_mask[y][x] == 2:
                    self.move_mask[y][x] = 1
        if move.mode == 'l':
            self.move_mask[(fy + ty) // 2][tx] = 2

    def is_attacked_field(self, y, x, color):  # color - цвет атакующего
        for ny in range(8):
            for nx in range(8):
                fig = self.get_fig(ny, nx, color)
                if fig is not None:
                    fields = fig.get_attacked_fields(ny, nx, self)
                    if (y, x) in fields:
                        return True
        return False

    def check_for_shah(self, color):  # color - цвет короля, шахи которому мы смотрим
        for y in range(8):
            for x in range(8):
                if self.get_fig(y, x, color) is not None and self.get_fig(y, x, color).key == 'K':

                    return self.is_attacked_field(y, x, enemy_color(color))

    def undo(self):
        if len(self.moves) > 0:
            moves = self.moves.copy()
            moves.pop()
            self._generate_new_field()
            for move in moves:
                self.perform_move(move)

    def get_val_moves(self, y, x, color):
        val_moves = []
        moves = self.get_moves(y, x, color)
        for move in moves:
            self.perform_move(move)
            if not self.check_for_shah(color):
                val_moves.append(move)
            self.undo()
        return val_moves

    def check_for_mate(self, color):  # color - цвет заматованого короля
        val_moves = 0
        for y in range(8):
            for x in range(8):
                val_moves += len(self.get_val_moves(y, x, color))

        if val_moves == 0:
            return self.check_for_shah(color)
        return False

    def change_pawn(self, key):
        self.moves[len(self.moves) - 1].extra_info = key

    def debug(self):
        pass


class StrangeBoard (Board):
    def _generate_new_field(self):
        self.moves = []
        self.board = [
            [RK(1), Knight(1), BK(1), QK(1), King(1), BK(1), Knight(1), RK(1)],
            [Pawn(1) for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Pawn(0) for x in range(8)],
            [RK(0), Knight(0), BK(0), QK(0), King(0), BK(0), Knight(0), RK(0)]
        ]
        self.move_mask = [[0 for x in range(8)] for y in range(8)]