import tkinter
import datetime as dt
import requests
import smtplib

FONT = ("Courier",20,"bold")
LATITUDE = 52.237049
LONGITUDE = 21.017532
MAP_HEIGHT = 640
MAP_WIDTH = 1280
PROXIMITY_THRESHOLD = 10

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("ISS Locator")
        self.minsize(1280,720)
        self.map_image = tkinter.PhotoImage(file="Images/world_map.png")
        self.satellite_image = tkinter.PhotoImage(file="Images/satellite.png")

        self.daytime = {
            "Day time": tkinter.PhotoImage(file="Images/sun.png"),
            "Nighttime": tkinter.PhotoImage(file="Images/moon.png")
        }

        self.build_canvas()
        self.build_labels()

    def build_canvas(self):
        self.canvas = tkinter.Canvas(self,width=MAP_WIDTH,height=MAP_HEIGHT)
        self.canvas_map_image = self.canvas.create_image(640, 300, image=self.map_image)
        self.canvas_satellite_image = self.canvas.create_image(0, 0, image=self.satellite_image)
        self.canvas.place(x=0,y=100)

    def build_labels(self):
        self.label1 = tkinter.Label(self,text="", font=FONT)
        self.label1.place(x=800,y=20)

        self.label2 = tkinter.Label(self,text=f"Location\nLatitude = {LATITUDE}\nLongitude = {LONGITUDE}" , font=FONT)
        self.label2.place(x=400,y=0)

        self.label3 = tkinter.Label(self,text="", font=FONT)
        self.label3.place(x=50,y=0)

        self.label4 = tkinter.Label(self,image=self.daytime["Day time"])
        self.label4.place(x=1100,y=10)

    def change_time_label(self):
        self.label1.config(text=f"Current time\n{dt.datetime.now().strftime("%d.%m.%Y %H:%M")}")

    def change_space_station_loc_label(self,lat,long):
        self.label3.config(text=f"ISS location\nLatitude ={lat}\nLongitude = {long} ")

    def change_label_image(self, state):
        self.label4.config(image=self.daytime[state])

    def move_iss(self,x,y):
        self.canvas.coords(self.canvas_satellite_image, x, y)

class Logic:
    def __init__(self, app, credentials):
        self.gui_app = app
        self.credentials_dict = credentials
        self.sunrise:int = 0
        self.sunset:int = 0
        self.day_state = ""
        self.get_sunrise_sunset_time()
        self.timer()

    def timer(self):
        self.gui_app.change_time_label()
        self.time_of_day()
        self.space_station_location_api()
        self.gui_app.after(60000,self.timer)

    def space_station_location_api(self):
        try:
            response = requests.get(self.credentials_dict["ISS_LOC_API"], timeout=30)
            data = response.json()
            lat, long = float(data["iss_position"]["latitude"]), float(data["iss_position"]["longitude"])
            self.gui_app.change_space_station_loc_label(lat, long)
            self.move_space_station_loc(long, lat)
            self.is_iss_nearby(lat, long)
        except requests.exceptions.ConnectTimeout:
            print("ISS API request timed out, will retry next cycle.")

    def move_space_station_loc(self,x,y):
        x_cor = (180 + x) * (MAP_WIDTH/360)
        y_cor = (90 - y) * (MAP_HEIGHT/180)

        self.gui_app.move_iss(x_cor,y_cor)

    def get_sunrise_sunset_time(self):
        parameters = {
            "lng": LONGITUDE,
            "lat": LATITUDE
        }
        response = requests.get(self.credentials_dict["SUNSET_SUNRISE_API"], params=parameters, timeout = 10)
        data = response.json()
        self.sunrise = int(data["sunrise"].split("T")[1].split(":")[0])
        self.sunset = int(data["sunset"].split("T")[1].split(":")[0])

    def time_of_day(self):
        if self.sunrise < dt.datetime.now().hour < self.sunset:
            self.day_state = "Day time"
        else:
            self.day_state = "Nighttime"
        self.gui_app.change_label_image(self.day_state)

    def is_iss_nearby(self,lat,long):
        """This method is invoked by another method whereby ISS api is invoked and its current location received.
        IF given condition -ISS is nearby lat, and long wise another method is invoked to see it is whether nighttime"""
        if lat - PROXIMITY_THRESHOLD <  LATITUDE < lat + PROXIMITY_THRESHOLD and long - PROXIMITY_THRESHOLD < LONGITUDE < long + PROXIMITY_THRESHOLD:
            self.is_iss_visible()

    def is_iss_visible(self):
        """This method only invoked when ISS is nearby to our location.
        To see the ISS it must be nighttime, and must be close to our location longitude and latitude wise.
        If it is nighttime and close to our location, send_mail method is invoked
        """
        if self.day_state == "Nighttime":
            self.send_mail()

    def send_mail(self):
        smtp_address = ""
        if "@gmail.com" in self.credentials_dict["EMAIL_SENDER"]:
            smtp_address = "smtp.gmail.com"
        elif "@yahoo.com" in self.credentials_dict["EMAIL_SENDER"]:
            smtp_address = "smtp.mail.yahoo.com"
        elif "@hotmail.com" in self.credentials_dict["EMAIL_SENDER"]:
            smtp_address = "smtp.live.com"
        else:
            print("Unknown address; check the mail address provider")

        with smtplib.SMTP(smtp_address) as connection:
            connection.starttls()
            connection.login(user=self.credentials_dict["EMAIL_SENDER"], password=self.credentials_dict["pass"])
            connection.sendmail(from_addr=self.credentials_dict["EMAIL_SENDER"],
                                to_addrs=self.credentials_dict["EMAIL_RECEIVER"],
                                msg="Subject:Look Up!\n\nISS passing above you!".encode("utf-8"))
