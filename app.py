import tkinter
import datetime as dt
import requests

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

        self.label3 = tkinter.Label(self,text="", font=FONT)
        self.label3.place(x=100,y=0)

    def change_time_label(self):
        self.label1.config(text=f"Current time\n{dt.datetime.now().strftime("%d.%m.%Y %H:%M")}")

    def change_space_station_loc_label(self,lat,long):
        self.label3.config(text=f"ISS location\nLatitude ={lat}\nLongitude = {long} ")

class Logic:
    def __init__(self, app, credentials):
        self.gui_app = app
        self.credentials_dict = credentials
        self.timer()


    def timer(self):
        self.gui_app.change_time_label()
        self.space_station_location_api()
        self.gui_app.after(60000,self.timer)

    def space_station_location_api(self):
        response = requests.get(self.credentials_dict["ISS_LOC_API"])
        data = response.json()
        lat,long = data["iss_position"]["latitude"],data["iss_position"]["longitude"]
        self.gui_app.change_space_station_loc_label(lat,long)