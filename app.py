import tkinter
import datetime as dt
import requests

FONT = ("Courier",20,"bold")
LATITUDE = 52.237049
LONGITUDE =  21.017532
MAP_HEIGHT = 640
MAP_WIDTH = 1280

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("ISS Locator")
        self.minsize(1280,720)
        self.map_image = tkinter.PhotoImage(file="Images/world_map.png")
        self.satellite_image = tkinter.PhotoImage(file="Images/satellite.png")

        self.build_canvas()
        self.build_labels()

    def build_canvas(self):
        self.canvas = tkinter.Canvas(self,width=MAP_WIDTH,height=MAP_HEIGHT)
        self.canvas_map_image = self.canvas.create_image(640, 300, image=self.map_image)
        self.canvas_satellite_image = self.canvas.create_image(0, 0, image=self.satellite_image)
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

    def move_iss(self,x,y):
        self.canvas.coords(self.canvas_satellite_image, x, y)

class Logic:
    def __init__(self, app, credentials):
        self.gui_app = app
        self.credentials_dict = credentials
        self.dx = 0
        self.dy = 0
        self.prev_x = 0
        self.prev_y = 0
        self.timer()

    def timer(self):
        self.gui_app.change_time_label()
        self.space_station_location_api()
        self.gui_app.after(60000,self.timer)

    def space_station_location_api(self):
        try:
            response = requests.get(self.credentials_dict["ISS_LOC_API"], timeout=30)
            data = response.json()
            lat, long = float(data["iss_position"]["latitude"]), float(data["iss_position"]["longitude"])
            self.gui_app.change_space_station_loc_label(lat, long)
            self.move_space_station_loc(long, lat)
        except requests.exceptions.ConnectTimeout:
            self.space_station_location_api()

    def move_space_station_loc(self,x,y):
        x_cor = (180 + x) * (MAP_WIDTH/360)
        y_cor = (90 - y) * (MAP_HEIGHT/180)

        self.gui_app.move_iss(x_cor,y_cor)
