from App import AppPiece, App, StrangeApp

d = {'Normal': App, 'New figs': StrangeApp, 'Piece': AppPiece}
app = None
while app is None:
    try:
        s = input(f'Во что поиграем? {", ".join(list(d.keys()))}\n')
        app = d[s]()
    except KeyError as e:
        print('Вы ввели что-то не то')

app.run()
