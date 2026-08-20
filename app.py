import tkinter

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("ISS Locator")
        self.minsize(1280,640)
        self.image = tkinter.PhotoImage(file="world_map.png")

        self.build_canvas()

    def build_canvas(self):
        self.canvas = tkinter.Canvas(self,width=1280,height=640)
        self.canvas_image = self.canvas.create_image(640,300,image=self.image)
        self.canvas.place(x=0,y=0)