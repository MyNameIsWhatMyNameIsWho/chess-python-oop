# Chess + Custom Figures (Python)

A terminal chess implementation for two players, extended with a **custom "new figures" game mode** featuring compound pieces not in standard chess. Built as an early exercise in OOP design and extensible class hierarchies.

**Language:** Python 3 · **Library:** colorama (colored terminal board)

---

## Game modes

| Mode | Description |
|------|-------------|
| **Classic** | Standard chess rules — all standard pieces, full move validation |
| **New Figures** | Adds compound pieces: **QK** (Queen+Knight), **RK** (Rook+Knight), **BK** (Bishop+Knight) |
| **Piece mode** | Special board with **Piece** and **PieceKing** — jump/capture rules on an alternate `PieceBoard` |

---

## Architecture

Piece behavior is defined by class inheritance — each piece type overrides `get_moves()` on the `Fig` base class. Adding a new piece type means creating a new subclass with its own movement logic; existing validation code doesn't change.

| File | Responsibility |
|------|---------------|
| `main.py` | Mode selection entry point |
| `App.py` | Game loop: move input, display, undo, danger check |
| `Board.py` | Board state, legal move validation, check/mate detection, undo stack |
| `Fig.py` | `Fig` base class + all piece subclasses (standard + custom) |
| `Move.py` | Move representation |
| `Converters.py` | Coordinate utilities |
| `PieceBoard.py` | Alternate board for Piece mode |

**Move validation:** `get_val_moves()` simulates each candidate move and discards any that leave the king in check — standard legal move filtering.

---

## How to run

```bash
pip install colorama
python main.py
```

Use keyboard input to select game mode and enter moves. The board is rendered in color in the terminal with legal move highlights.
