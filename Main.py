from tkinter import *
from tkinter import ttk
from controller import Controller

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, position: Point, radius: float):
        self.position = position
        self.radius = radius

class Application(ttk.Frame):

    @classmethod
    def main(cls):
        NoDefaultRoot()
        root = Tk()
        app = cls(root)
        app.grid(sticky=N)
        root.title("Fake Controller")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.resizable(False, False)
        root.mainloop()

    def __init__(self, root: Tk):
        super().__init__(root, padding="20 20 20 20")
        self.create_variables()
        self.create_widgets()
        self.grid_widgets()
        self.grid_columnconfigure(0, weight=1)
        root.update()
        self.draw_circle(70)
        self.draw_rect(5)
    
    def create_variables(self):
        self.status = StringVar(self, "Status")

    def create_widgets(self):
        self.up_btn = ttk.Button(self, text="▲")
        self.down_btn = ttk.Button(self, text="▼")
        self.left_btn = ttk.Button(self, text="◄")
        self.right_btn = ttk.Button(self, text="►")
        self.a_btn = ttk.Button(self, text="A")
        self.b_btn = ttk.Button(self, text="B")
        self.canvas = Canvas(self, width=200, height=200)
    
    def grid_widgets(self):
        self.up_btn.grid(row=0, column=1, sticky=S, ipady=15)
        self.down_btn.grid(row=2, column=1, sticky=N, ipady=15)
        self.left_btn.grid(row=1, column=0, sticky=E, ipady=15)
        self.right_btn.grid(row=1, column=2, sticky=W, ipady=15)
        self.a_btn.grid(row=1, column=3, padx=(10, 0), ipady=15)
        self.b_btn.grid(row=1, column=4, ipady=15)
        self.canvas.grid(row=0, rowspan=3, column=5, columnspan=2, padx=15)

    def draw_circle(self, radius: int):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.create_oval(w/2-radius, h/2-radius, 
                                w/2+radius, h/2+radius, 
                                fill="#fff", width=2)
        self.circle = Circle(Point(w/2, h/2), radius)
    
    def draw_rect(self, size: int):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.rectangle = self.canvas.create_rectangle(w/2-size, h/2-size, 
                                     w/2+size, h/2+size, 
                                     fill="#000")

    def move_rectangle(self):
        pass

    def reset_rectangle(self):
        pass



def is_in_circle(circle: Circle, position: Point) -> bool:
    return (position.x - circle.position.x)**2 + (position.y - circle.position.y)**2 <= circle.radius**2



if __name__ == "__main__":
    Application.main()