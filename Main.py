from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from bt_connection import ControllerConnection
from bt_connection import Device
from os.path import exists

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
        root.protocol('WM_DELETE_WINDOW', app.on_quit)
        root.mainloop()
    
    def __init__(self, root: Tk):
        super().__init__(root, padding="0 0 0 0")
        self.root = root
        self.create_variables()
        self.history_filename = ".history"
        self.load_history()
        self.create_widgets()
        self.grid_widgets()
        
    def received(self, message: bytes):
        self.set_status("recieved " + message.decode("utf-8"))

    def create_variables(self):
        self.status = StringVar(self, "Status: disconnected")
        self.controller = ControllerConnection()
        

    def load_history(self):
        self.history = None
        if not exists(self.history_filename):
            return
        history = open(self.history_filename, 'r')
        dev = history.readline()
        if dev.strip() != "":
            dev = dev.split(",")
            self.history = Device(dev[0], dev[1])  

    def set_status(self, value: str):
        self.status.set("Status: " + value)
        
    def create_widgets(self):
        self.control = Control(self)
        self.status_lb = ttk.Label(self, textvariable=self.status, anchor=W, relief=SUNKEN)
        self.menu = Menu(self)
        self.bluetooth_menu = Menu(self.menu, tearoff=0)
        self.device_menu = Menu(self.bluetooth_menu, tearoff=0)
        if self.history is not None:
            self.device_menu.add_command(label=self.history.name, command=lambda: self.connect(self.history))
        self.menu.add_cascade(label="Bluetooth", menu=self.bluetooth_menu)
        self.bluetooth_menu.add_command(label="Search devices", command=self.search)
        self.bluetooth_menu.add_cascade(label="Select device", menu=self.device_menu)
        self.bluetooth_menu.add_command(label="Disconnect", state="disabled", command=self.controller.disconnect)
        self.bluetooth_menu.add_separator()
        self.bluetooth_menu.add_command(label="Exit", command=self.on_quit)
        self.root.config(menu=self.menu)

    def grid_widgets(self):
        self.control.grid(row=0, column=0, columnspan=7, rowspan=3, sticky=NSEW)
        self.status_lb.grid(row=3, column=0, columnspan=7, sticky=NSEW)
    
    def send(self, value: str):
        self.controller.send(value)
    
    def search(self):
        self.set_status("searching...")
        n = self.controller.search_devices()
        self.set_status("found " + str(n) + " devices")
        if n > 0:
            self.set_disconnect_enabled(True)
            for device in self.controller.devices:
                self.device_menu.add_command(label=device.name, command=lambda: self.connect(device))
    
    def set_disconnect_enabled(self, enabled: bool):
        value = "normal"
        if not enabled:
            value = "disabled"
        self.bluetooth_menu.entryconfig("Disconnect", state=value)
    
    def connect(self, device: Device):
        self.set_status("connecting to " + device.name)
        if self.controller.connect(device):
            self.set_status("connected to " + device.name)
            self.controller.start_receiving(self.received)
            self.history = device
        else:
            self.set_status("connection failed")
            
    def on_quit(self):
        if self.history is not None:
            history = open(self.history_filename, 'w')
            history.write(self.history.name + "," + self.history.address)
            history.close()
        self.controller.disconnect()
        self.root.quit()

        
class Control(ttk.Frame):

    def __init__(self, root: Application):
        super().__init__(root, padding="20 20 20 20")
        self.app = root
        self.create_variables()
        self.create_widgets()
        self.grid_widgets()
        root.update()
        self.draw_circle(50)
        self.draw_rect(5)
    
    def create_variables(self):
        pass

    def create_widgets(self):
        self.up_btn = ttk.Button(self, text="▲", command=lambda: self.app.send("up"))
        self.down_btn = ttk.Button(self, text="▼", command=lambda: self.app.send("down"))
        self.left_btn = ttk.Button(self, text="◄", command=lambda: self.app.send("left"))
        self.right_btn = ttk.Button(self, text="►", command=lambda: self.app.send("right"))
        self.a_btn = ttk.Button(self, text="A", command=lambda: self.app.send("a"))
        self.b_btn = ttk.Button(self, text="B", command=lambda: self.app.send("b"))
        self.canvas = Canvas(self, width=200, height=200)
        self.canvas.bind("<B1-Motion>", self.move_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.reset_rectangle)
        
    def grid_widgets(self):
        self.up_btn.grid(row=0, column=1, sticky=S, ipady=15)
        self.down_btn.grid(row=2, column=1, sticky=N, ipady=15)
        self.left_btn.grid(row=1, column=0, sticky=E, ipady=15, padx=(10, 0))
        self.right_btn.grid(row=1, column=2, sticky=W, ipady=15)
        self.a_btn.grid(row=1, column=3, padx=(10, 0), ipady=15)
        self.b_btn.grid(row=1, column=4, ipady=15)
        self.canvas.grid(row=0, rowspan=3, column=5, columnspan=2, padx=15, sticky=NSEW)        

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
        coords = self.canvas.coords(self.rectangle)
        self.initial_rect = (coords[0], coords[1], size)

    def move_rectangle(self, event):
        (x, y, size) = self.initial_rect
        if is_in_circle(self.circle, Point(event.x, event.y)):
            self.app.send((event.x - (x+size), event.y - (y+size)))
            self.canvas.moveto(self.rectangle, event.x - size, event.y - size)
        
    def reset_rectangle(self, event):
        (x, y, _size) = self.initial_rect
        self.canvas.moveto(self.rectangle, x, y)

def is_in_circle(circle: Circle, position: Point) -> bool:
    return (position.x - circle.position.x)**2 + (position.y - circle.position.y)**2 <= circle.radius**2


if __name__ == "__main__":
    Application.main()
