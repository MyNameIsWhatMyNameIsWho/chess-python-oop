from Board import Board, StrangeBoard
from PieceBoard import PieceBoard
from Converters import m2c, enemy_color


class App:
    def __init__(self):
        self.player = 1
        self.board = Board()
        self.moves = []

    def choose(self, args):
        y, x = m2c(args[1])
        self.moves = self.board.get_val_moves(y, x, self.player)
        return 'Выбор сделан' #'\n'.join(map(str, self.moves))

    def show(self, args):
        if len(args) == 2:
            return self.board.show(for_player=self.player, moves=self.moves)
        else:
            return self.board.show(for_player=self.player)

    def move(self, args):
        y, x = m2c(args[1])
        for move in self.moves:
            if move.tx == x and move.ty == y:
                ans = self.board.perform_move(move)
                if ans == 'pawn':
                    self.change_pawn()
                self.player = enemy_color(self.player)
                self.moves = []

                if self.board.check_for_mate(self.player):
                    return f'{"Белые" if self.player == 1 else "Черные"} получают мат!'
                return 'Ход выполнен. Ходит следующий игрок'
        return 'Нельзя так ходить'

    def undo(self, args):
        if len(self.board.moves) > 0:
            self.board.undo()
            self.player = enemy_color(self.player)
            self.moves = []
            return 'Отмена'
        return 'Не отмена'

    def danger(self, args):
        return self.board.danger(self.player)

    def change_pawn(self):
        print('Замена пешки: введите новыю фигуру Q, N, R, B')
        req = input()
        while req not in ('Q', 'R', 'B', 'N'):
            print('Проверка на дурака')
            req = input()
        self.board.change_pawn(req)

    def debug(self, commands):
        funcs = {'C': self.choose, 'S': self.show, 'M': self.move, 'U': self.undo, 'D' : self.danger}
        for command in commands.split('\n'):
            print(command)
            args = command.split()
            print(funcs[args[0]](args))

    def run(self):
        print('''
Посмотреть на поле - S
Выбор фигуры - C <координаты фигуры>
Посмотреть на возможные ходы - S M
Посмотреть на угрозы - D
Переставить выбранную фигуру - M <координаты клетки>
Отмена хода - U
Пряитной игры!!!
        ''')
        funcs = {'C': self.choose, 'S': self.show, 'M': self.move, 'U': self.undo, 'D': self.danger}
        command = ''
        while command != 'E':
            command = input()
            args = command.split()
            if args[0] in funcs.keys():
                print(funcs[args[0]](args))
            else:
                print('Неверная команда')


class AppPiece(App):
    def __init__(self):
        super().__init__()
        self.board = PieceBoard()
        self.blocked = False

    def move(self, args):
        y, x = m2c(args[1])
        for move in self.moves:
            if move.tx == x and move.ty == y:
                ans = self.board.perform_move(move)
                self.moves = [] if not ans else self.board.get_val_moves(y, x, self.player)
                self.player = enemy_color(self.player) if not ans else self.player
                self.blocked = ans
                return 'Ход выполнен. Ходит следующий игрок' if not ans else 'Продолжайте есть!'

    def choose(self, args):
        if not self.blocked:
            return super().choose(args)
        else:
            return 'Продолжайте есть!'


class StrangeApp (App):
    def __init__(self):
        super().__init__()
        self.board = StrangeBoard()
