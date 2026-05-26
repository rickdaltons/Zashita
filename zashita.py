import tkinter as tk
from tkinter import messagebox


EMPTY_CELL = 0
PLAYER_CELL = "P"
WALL_CELL = "W"
COIN_CELL = "C"
FINISH_CELL = "F"

CELL_SIZE = 60
ROWS = 6
COLUMNS = 6


class GameBoard:
    """Stores and changes the game field."""

    def __init__(self):
        """Initialize the game board."""
        self.field = self.create_field()
        self.player_position = (0, 0)
        self.coins_collected = 0

    def create_field(self):
        """Create a two-dimensional game field."""
        return [
            [PLAYER_CELL, EMPTY_CELL, EMPTY_CELL, WALL_CELL, EMPTY_CELL, EMPTY_CELL],
            [EMPTY_CELL, WALL_CELL, EMPTY_CELL, WALL_CELL, COIN_CELL, EMPTY_CELL],
            [EMPTY_CELL, WALL_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
            [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, WALL_CELL, WALL_CELL, EMPTY_CELL],
            [COIN_CELL, WALL_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
            [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, WALL_CELL, EMPTY_CELL, FINISH_CELL],
        ]

    def get_cell(self, row, column):
        """Return the value of a cell."""
        return self.field[row][column]

    def is_inside_board(self, row, column):
        """Check if the position is inside the game board."""
        return 0 <= row < ROWS and 0 <= column < COLUMNS

    def is_wall(self, row, column):
        """Check if the cell is a wall."""
        return self.field[row][column] == WALL_CELL

    def move_player(self, row_offset, column_offset):
        """Move the player if the target cell is available."""
        current_row, current_column = self.player_position
        new_row = current_row + row_offset
        new_column = current_column + column_offset

        if not self.is_inside_board(new_row, new_column):
            return False

        if self.is_wall(new_row, new_column):
            return False

        target_cell = self.field[new_row][new_column]

        if target_cell == COIN_CELL:
            self.coins_collected += 1

        self.field[current_row][current_column] = EMPTY_CELL
        self.field[new_row][new_column] = PLAYER_CELL
        self.player_position = (new_row, new_column)

        return target_cell == FINISH_CELL


class GameView:
    """Draws the game field on the screen."""

    def __init__(self, root, board):
        """Initialize the game view."""
        self.root = root
        self.board = board

        self.canvas = tk.Canvas(
            root,
            width=COLUMNS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="white",
        )
        self.canvas.pack(pady=10)

        self.info_label = tk.Label(
            root,
            text="Собрано монет: 0",
            font=("Arial", 14),
        )
        self.info_label.pack()

    def draw_board(self):
        """Draw all cells of the game board."""
        self.canvas.delete("all")

        for row in range(ROWS):
            for column in range(COLUMNS):
                cell_value = self.board.get_cell(row, column)
                self.draw_cell(row, column, cell_value)

        self.update_info()

    def draw_cell(self, row, column, value):
        """Draw one cell."""
        x1 = column * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        color = self.get_cell_color(value)

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            outline="black",
        )

        if value != EMPTY_CELL:
            self.canvas.create_text(
                x1 + CELL_SIZE / 2,
                y1 + CELL_SIZE / 2,
                text=value,
                font=("Arial", 20, "bold"),
            )

    def get_cell_color(self, value):
        """Return the color for a cell value."""
        colors = {
            EMPTY_CELL: "white",
            PLAYER_CELL: "lightblue",
            WALL_CELL: "gray",
            COIN_CELL: "gold",
            FINISH_CELL: "lightgreen",
        }

        return colors.get(value, "white")

    def update_info(self):
        """Update information about collected coins."""
        self.info_label.config(
            text=f"Собрано монет: {self.board.coins_collected}"
        )


class GameController:
    """Handles user actions."""

    def __init__(self, root, board, view):
        """Initialize the game controller."""
        self.root = root
        self.board = board
        self.view = view

        self.bind_keys()

    def bind_keys(self):
        """Bind keyboard buttons to movement."""
        self.root.bind("<Up>", lambda event: self.handle_move(-1, 0))
        self.root.bind("<Down>", lambda event: self.handle_move(1, 0))
        self.root.bind("<Left>", lambda event: self.handle_move(0, -1))
        self.root.bind("<Right>", lambda event: self.handle_move(0, 1))

    def handle_move(self, row_offset, column_offset):
        """Handle player movement."""
        is_finished = self.board.move_player(row_offset, column_offset)
        self.view.draw_board()

        if is_finished:
            messagebox.showinfo(
                "Победа",
                f"Вы дошли до финиша!\nСобрано монет: {self.board.coins_collected}",
            )
            self.root.destroy()


class GameApplication:
    """Starts and manages the application."""

    def __init__(self):
        """Initialize the game application."""
        self.root = tk.Tk()
        self.root.title("Игровое поле")

        self.board = GameBoard()
        self.view = GameView(self.root, self.board)
        self.controller = GameController(self.root, self.board, self.view)

    def run(self):
        """Run the application."""
        self.view.draw_board()
        self.root.mainloop()


def main():
    """Create and start the game."""
    application = GameApplication()
    application.run()


if __name__ == "__main__":
    main()