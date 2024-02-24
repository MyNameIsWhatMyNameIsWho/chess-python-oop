from Board import Board
from Fig import Piece, Empty, PieceKing


class PieceBoard(Board):
    def _generate_new_field(self):
        self.moves = []
        self.board = [
            [Piece(1), Empty(), Piece(1), Empty(), Piece(1), Empty(), Piece(1), Empty()],
            [Empty(), Piece(1), Empty(), Piece(1), Empty(), Piece(1), Empty(), Piece(1)],
            [Piece(1), Empty(), Piece(1), Empty(), Piece(1), Empty(), Piece(1), Empty()],
            [Empty() for x in range(8)],
            [Empty() for x in range(8)],
            [Empty(), Piece(0), Empty(), Piece(0), Empty(), Piece(0), Empty(), Piece(0)],
            [Piece(0), Empty(), Piece(0), Empty(), Piece(0), Empty(), Piece(0), Empty()],
            [Empty(), Piece(0), Empty(), Piece(0), Empty(), Piece(0), Empty(), Piece(0)]

        ]
        self.move_mask = [[0 for x in range(8)] for y in range(8)]

    def perform_move(self, move):
        super().perform_move(move)
        if move.mode == 'x':
            if move.key == 'k':
                ny, nx = move.fy, move.fx
                dy = (move.ty - move.fy) // abs(move.ty - move.fy)
                dx = (move.tx - move.fx) // abs(move.tx - move.fx)
                while self.is_empty_field(ny, nx):
                    ny += dy
                    nx += dx
                self.board[ny][nx] = Empty()
            else:
                self.board[(move.ty + move.fy) // 2][(move.tx + move.fx) // 2] = Empty()

        if move.extra_info == 'K':
            self.board[move.ty][move.tx] = PieceKing(move.ty // 7)

        return len(self.get_val_moves(move.ty, move.tx, self.get_fig(move.ty, move.tx).color)) and move.mode == 'x'

    def get_val_moves(self, y, x, color):
        can_eat = False
        for ny in range(8):
            for nx in range(8):
                for m in self.get_moves(ny, nx, color):
                    if m.mode == 'x':
                        can_eat = True
        if can_eat:
            val_moves = []
            for move in self.get_moves(y, x, color):
                if move.mode == 'x':
                    val_moves.append(move)
            return val_moves
        return self.get_moves(y, x, color)

    def check_for_shah(self, color):
        pass

    def check_for_mate(self, color):
        pass