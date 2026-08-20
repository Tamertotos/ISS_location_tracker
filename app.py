import tkinter

FONT = ("Courier",20,"bold")
LATITUDE = 52.237049
LONGITUDE =  21.017532

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("ISS Locator")
        self.minsize(1280,720)
        self.image = tkinter.PhotoImage(file="world_map.png")

        self.build_canvas()
        self.build_labels()

    def build_canvas(self):
        self.canvas = tkinter.Canvas(self,width=1280,height=640)
        self.canvas_image = self.canvas.create_image(640,300,image=self.image)
        self.canvas.place(x=0,y=100)

    def build_labels(self):
        self.label1 = tkinter.Label(self,text= "Current Timee\n123", font=FONT)
        self.label1.place(x=900,y=0)

        self.label2 = tkinter.Label(self,text=f"Location\nLatitude = {LATITUDE}\nLongitude = {LONGITUDE}" , font=FONT)
        self.label2.place(x=500,y=0)
    