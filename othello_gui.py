import Tkinter as tk
from othello_controller import OthelloPlayer, OthelloController

class BoardGUITk(tk.Frame):
    rows = 8
    columns = 8

    @property
    def canvas_size(self):
        return (self.columns * self.square_size, self.rows * self.square_size)

    def __init__(self, parent, controller, square_size=64):
        self.controller = controller
        self.square_size = square_size
        self.parent = parent

        canvas_width = self.columns * square_size
        canvas_height = self.rows * square_size

        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background='grey')
        self.canvas.pack(side='top', fill='both', anchor='c', expand=True)

        self.canvas.bind('<Configure>', self.refresh)
        self.canvas.bind('<Button-1>', self.click)

        self.statusbar = tk.Frame(self, height=64)

        self.label_status = tk.Label(self.statusbar, text='   White\'s turn  ', fg='black')
        self.label_status.pack(side=tk.LEFT, expand=0, in_=self.statusbar)

    def click(self, event):
        col_size = row_size = event.widget.master.square_size

        current_column = event.x / col_size
        current_row = 7 - (event.y / row_size)

        self.move(current_column, current_row)
        self.refresh()
        self.controller.play()
        self.refresh()

    def move(self, x, y):
        success = self.controller.make_move(x, y)                        
        if not success:               
            self.label_status['text'] = '   Illegal move   '

    def refresh(self, event={}):
        if event:
            xsize = int((event.width-1) / self.columns)
            ysize = int((event.height-1) / self.rows)
            self.square_size = min(xsize, ysize)
        self.canvas.delete('square')
        self.canvas.delete('piece')
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.square_size)
                y1 = ((7-row) * self.square_size)
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='green', tags='square')
                if self.controller.get_color(col, row) == 'b':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill='black', tags='piece')
                elif self.controller.get_color(col, row) == 'w':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill='white', tags='piece')
        if self.controller.player_to_move() == 'b':
            self.label_status['text'] = '   Black\'s turn   '
        else:
            self.label_status['text'] = '   White\'s turn   '
        self.canvas.tag_raise('piece')

def display(controller):
    root = tk.Tk()
    root.title('Python Othello')

    gui = BoardGUITk(root, controller)
    gui.pack(side='top', fill='both', expand='true', padx=4, pady=4)
    gui.refresh()

    root.mainloop()

if __name__=='__main__':
    player1 = OthelloPlayer('w', False)
    player2 = OthelloPlayer('b', True)
    board = OthelloController(player1, player2)
    display(board)

