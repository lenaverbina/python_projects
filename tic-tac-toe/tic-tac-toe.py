import tkinter as tk

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.frame, bg='white', height=300, width=300)
        self.pc_butt = tk.Button(self.frame, text="Начать новую игру",
                             width=30, command=board.init_game)

        self.lbl = tk.Label(text="Играем в крестики-нолики")
        self.rects = []
        self.canvas.pack()
        self.pc_butt.pack()
        self.lbl.pack()
        self.frame.pack()

    def create_rects(self):
        colors = ['red', 'yellow', 'green', 'pink', 'brown', 'grey', 'orange', 'purple', 'beige']
        count = -1
        rect_dict = {}
        # canvas.pack()
        for i in range(3):
            for j in range(3):
                count += 1
                rect = self.canvas.create_rectangle(i * 100, j * 100, i * 100 + 100, j * 100 + 100, fill=colors[count],
                                               outline='blue')
                key = 'rect' + str(i + 1) + str(j + 1)
                rect_dict[key] = rect
                self.canvas.tag_bind(rect_dict[key], '<ButtonPress-1>', lambda event: self.onObjectClick(event))

    def create_cross(self, coords):
        self.canvas.create_line(coords[0], coords[1], coords[2], coords[3], fill="black")
        self.canvas.create_line(coords[2], coords[1], coords[0], coords[3], fill="black")

    def create_circle(self, coords):
        self.canvas.create_oval(coords[0], coords[1], coords[2], coords[3], outline='blue')

    @staticmethod
    def matrix_index(item):
        i = (item - 1) % 3
        j = (item - 1) // 3
        return i, j

    def onObjectClick(self, event):
        if not board.end_game:
            item = self.canvas.find_closest(event.x, event.y)[0]
            coordinates = self.canvas.coords(item)
            i, j = self.matrix_index(item)
            if player.player_turn == 1 and board.game_board_matrix[i][j] == -1:
                self.create_cross(coordinates)
                self.canvas.itemconfig(item, fill="white")
                board.change_cell_value(i, j)
                board.game_count += 1
            elif player.player_turn == 2 and board.game_board_matrix[i][j] == -1:
                self.create_circle(coordinates)
                self.canvas.itemconfig(item, fill="white")
                board.change_cell_value(i, j)
                board.game_count += 1
            board.game_state()
            if board.winner != '':
                self.lbl.config(text=board.winner)
                board.end_game = True
            print(board.game_board_matrix)

class Board:
    def __init__(self):
        self.game_board_matrix = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]# -1 - пустая клетка, 1 - крестик, 0 - нолик
        self.game_count = 0
        self.winner = ''
        self.end_game = False

    def init_game(self):
        self.__init__()
        player.player_turn = 1
        for elem in root.winfo_children():
            elem.destroy()
        app = MainApplication(root)
        app.create_rects()

    def change_cell_value(self, i, j):
        if player.player_turn == 1:
            self.game_board_matrix[i][j] = 1
        else:
            self.game_board_matrix[i][j] = 0
        player.change_player_turn()

    def row_check(self):
        for row in self.game_board_matrix:
            if row[0] == 1 and len(set(row)) == 1:
                self.winner = "Игрок 1 выиграл"
            elif row[0] == 0 and len(set(row)) == 1:
                self.winner = "Игрок 2 выиграл"

    def column_check(self):
        for i in range(3):
            if self.game_board_matrix[0][i] == self.game_board_matrix[1][i] == self.game_board_matrix[2][i] == 1:
                self.winner = "Игрок 1 выиграл"
            elif self.game_board_matrix[0][i] == self.game_board_matrix[1][i] == self.game_board_matrix[2][i] == 0:
                self.winner = "Игрок 2 выиграл"


    def diagonal_check(self):
        diag1 = [self.game_board_matrix[i][i] for i in range(3)]
        diag2 = [self.game_board_matrix[2 - i][i] for i in
                 range(3)]  # length - 1 - i для первого индекса обратной диагонали, length = 3
        if len(set(diag1)) == 1 and diag1[0] == 1:
            self.winner = "Игрок 1 выиграл"
        elif len(set(diag2)) == 1 and diag2[0] == 1:
            self.winner = "Игрок 1 выиграл"
        elif len(set(diag1)) == 1 and diag1[0] == 0:
            self.winner = "Игрок 2 выиграл"
        elif len(set(diag2)) == 1 and diag2[0] == 0:
            self.winner = "Игрок 2 выиграл"

    def game_state(self):
        if self.game_count == 9:
            self.winner = 'Ничья'
        elif 4 < self.game_count < 9:
            self.row_check()
            if self.winner == '':
                self.column_check()
                if self.winner == '':
                    self.diagonal_check()

class Player:
    def __init__(self):
        self.player_turn = 1
    def change_player_turn(self):
        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1

if __name__ == "__main__":
    board = Board()
    player = Player()
    root = tk.Tk()
    root.resizable(False, False)
    app = MainApplication(root)
    app.create_rects()
    root.mainloop() #наша игра

