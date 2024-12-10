# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
from random import randrange

player1_turn = True

class CanvasData():
    def __init__(self):
        self.prev_width = -1
        self.prev_height = -1
        self.cur_width = -1
        self.cur_height = -1

def init_game():
    # root.unbind_all()
    for elem in root.winfo_children():
        elem.destroy()
    myframe = Frame(root)
    myframe.pack(fill=BOTH, expand=YES)
    canvas = Canvas(myframe, bg='white', height=300, width=300)
    canvas.pack(fill=BOTH, expand=YES)
    pc_butt = ttk.Button(myframe, text="Начать новую игру",
                         width=30, command=init_game)  # Создаем кнопку хода компьютера с шириной в 30 пикселей
    pc_butt.pack(fill=BOTH, expand=YES)  # изменять координаты при window redraw/resize
    lbl = ttk.Label(text="Играем в крестики-нолики")
    lbl.pack()
    rect_dict = {}
    colors = ['red', 'yellow', 'green', 'pink', 'brown', 'grey', 'orange', 'purple', 'beige']
    count = -1
    # canvas.pack()
    for i in range(3):
        for j in range(3):
            count += 1
            rect = canvas.create_rectangle(i*100, j*100, i*100+100, j*100+100, fill=colors[count], outline='blue')
            key = 'rect' + str(i+1) + str(j+1)
            rect_dict[key] = rect
            canvas.tag_bind(rect_dict[key], '<ButtonPress-1>', lambda event: onObjectClick(event, canvas, lbl))
            print(rect)
    print(rect_dict)
    onObjectClick.player1_turn = True
    onObjectClick.game_board_matrix = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    onObjectClick.end_game = False
    onObjectClick.moves = 0
    if onObjectClick.player1_turn is False:
        computer_click()


def create_cross(canvas, coords):
    canvas.create_line(coords[0], coords[1], coords[2], coords[3], fill="black")
    canvas.create_line(coords[2], coords[1], coords[0], coords[3], fill="black")


def create_circle(canvas, coords):
    canvas.create_oval(coords[0], coords[1], coords[2], coords[3], outline='blue')


def row_check(game_board_mat):  # проверяем одинаковые элементы по строкам
    winner = ''
    for row in game_board_mat:
        if row[0] == 1 and len(set(row)) == 1:
            winner = "Игрок 1 выиграл"
        elif row[0] == 0 and len(set(row)) == 1:
            winner = "Игрок 2 выиграл"
    return winner


def column_check(game_board_mat):  # проверяем одинаковые элементы по столбцам
    winner = ''
    for i in range(3):
        if game_board_mat[0][i] == game_board_mat[1][i] == game_board_mat[2][i] == 1:
            winner = "Игрок 1 выиграл"
        elif game_board_mat[0][i] == game_board_mat[1][i] == game_board_mat[2][i] == 0:
            winner = "Игрок 2 выиграл"
    return winner


def diagonal_check(game_board_mat):  # проверяем одинаковые элементы по диагоналям
    winner = ''
    diag1 = [game_board_mat[i][i] for i in range(3)]
    diag2 = [game_board_mat[2 - i][i] for i in
             range(3)]  # length - 1 - i для первого индекса обратной диагонали, length = 3
    if len(set(diag1)) == 1 and diag1[0] == 1:
        winner = "Игрок 1 выиграл"
    elif len(set(diag2)) == 1 and diag2[0] == 1:
        winner = "Игрок 1 выиграл"
    elif len(set(diag1)) == 1 and diag1[0] == 0:
        winner = "Игрок 2 выиграл"
    elif len(set(diag2)) == 1 and diag2[0] == 0:
        winner = "Игрок 2 выиграл"
    return winner


def game_state(game_board_mat):
    inf = row_check(game_board_mat)
    if inf == '':
        inf = column_check(game_board_mat)
        if inf == '':
            inf = diagonal_check(game_board_mat)
    return inf


def matrix_index(item):
    i = (item - 1) % 3
    j = (item - 1) // 3
    return i, j

def onObjectClick(event, canvas, lbl):
    if not onObjectClick.end_game:
        print('Got object click', event.x, event.y)
        item = canvas.find_closest(event.x, event.y)[0]
        coords = canvas.coords(item)
        i, j = matrix_index(item)
        if canvas.itemcget(item, "fill") == "white":
            return
        if onObjectClick.player1_turn:
            create_cross(canvas, coords)
            onObjectClick.game_board_matrix[i][j] = 1
            onObjectClick.player1_turn = False
            onObjectClick.moves += 1
            #tag = canvas.gettags(item)[0]
            canvas.itemconfig(item, fill="white")
            gs = game_state(onObjectClick.game_board_matrix)
            if gs != '':
            # canvas.destroy() #можно поставить флаг, который деактивирует игру
                lbl.config(text=gs)
                onObjectClick.end_game = True
        if onObjectClick.moves < 9:
            item = randrange(1, 9)
            i, j = matrix_index(item)
            while onObjectClick.game_board_matrix[i][j] != -1:
                item = randrange(1, 9)
                i, j = matrix_index(item)
            coords = canvas.coords(item)
            print(coords)
            create_circle(canvas, coords)
            onObjectClick.game_board_matrix[i][j] = 0
            onObjectClick.player1_turn = True
            onObjectClick.moves += 1
            gs = game_state(onObjectClick.game_board_matrix)
            if gs != '':
            # canvas.destroy() #можно поставить флаг, который деактивирует игру
                lbl.config(text=gs)
                onObjectClick.end_game = True
        #tag = canvas.gettags(item)[0]
            canvas.itemconfig(item, fill="white")
        else:
            if gs == '':
                lbl.config(text="Ничья")
                onObjectClick.end_game = True
            else:
                lbl.config(text=gs)
                onObjectClick.end_game = True
            #print("Количество ходов:", onObjectClick.moves)
            print(coords)
            print(onObjectClick.game_board_matrix)
    else:
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    root.title("tic-tac-toe")
    root.geometry("300x350")
    # root.resizable(0, 0)
    init_game()

    root.mainloop()

"""
    clicks = 0
    def click_button():
        global clicks
        if b["text"] == '':
            if clicks % 2 == 0:
                b["text"] = "X"
                clicks += 1
            else:
                b["text"] = "O"
                clicks += 1


    buttons = []

    #canvas.create_window(15, 66, anchor=NW, window=btn, width=50, height=59)



    #image = ttk.(file="image.png")
"""
# TODO:проверить, что поле заполнено либо через массив путем смены флага или по полю fill == white
# TODO: 2. написать логику выигрыша
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

#TODO:проверить, что поле заполнено либо через массив путем смены флага или по полю fill == white
#TODO: 2. написать логику выигрыша
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
