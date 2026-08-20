import tkinter
import datetime as dt

FONT = ("Courier",20,"bold")
LATITUDE = 52.237049
LONGITUDE =  21.017532

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("ISS Locator")
        self.minsize(1280,720)
        self.image = tkinter.PhotoImage(file="Images/world_map.png")

        self.build_canvas()
        self.build_labels()

    def build_canvas(self):
        self.canvas = tkinter.Canvas(self,width=1280,height=640)
        self.canvas_image = self.canvas.create_image(640,300,image=self.image)
        self.canvas.place(x=0,y=100)

    def build_labels(self):
        self.label1 = tkinter.Label(self,text="", font=FONT)
        self.label1.place(x=900,y=20)

        self.label2 = tkinter.Label(self,text=f"Location\nLatitude = {LATITUDE}\nLongitude = {LONGITUDE}" , font=FONT)
        self.label2.place(x=500,y=0)

    def change_text(self):
        self.label1.config(text=f"Current time\n{dt.datetime.now().strftime("%d.%m.%Y %H:%M")}")

class Logic:
    def __init__(self, app):
        self.gui_app = app
        self.timer()

    def timer(self):
        self.gui_app.change_text()
        self.gui_app.after(60000,self.timer)
