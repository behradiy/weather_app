''' DEVELOPED BY MIRACLE TEAM '''
from configparser import ConfigParser
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
import requests
import funcs
import time
import datetime
from datetime import datetime



#Getting url and api key from 'config.ini' file 
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']
url = config['url']['url']




def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (city, country, temp_celcius, temp_fahrenheit, icons, weather, description_weather, time,
        #  sunrise, sunset, pressure, min_temp, max_temp, wind_speed)
        city = json['name']
        country = json['sys']['country']
        temp_celcius = json['main']['temp'] - 273.15
        temp_fahrenheit = temp_celcius * 9 / 5 + 32
        icons = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        description_weather = json['weather'][0]['description']
        time = json['timezone']
        # more Details #
        sunrise = json["sys"]["sunrise"]
        sunset = json["sys"]["sunset"]
        min_temp = json["main"]["temp_min"]
        max_temp = json["main"]["temp_max"]

        final = (city, country, temp_celcius, temp_fahrenheit, icons, weather, description_weather, time,
                sunrise, sunset, min_temp, max_temp)
        funcs.Data_Base((city, country, temp_celcius, temp_fahrenheit, weather, time))
        return final

    else:
        return None


class MyWeatherApp():
    def __init__(self, window):
        self.window = window
        self.window.title("Weather App")
        self.window.geometry("450x500+100+80")
        self.window.configure(bg="white", padx=1, pady=1)
        title = Label(self.window,
            text="We show you,weather",
            font=("mincho", 25, 'italic'),
            relief=RAISED,
            bg="#15317E", fg="#FFFFFF").place(
            x=0,
            y=0,
            relwidth=1,
            height=60)

        # Search Entry#
        self.city_text = StringVar()
        
        lbl_city = Label(self.window, text="",
                        relief=RAISED, bg="#15317E",
                        fg="#FFFFFF", anchor="w", padx=5).place(x=0, y=60,relwidth=1, height=40)
                        
        self.city_entry = Entry(self.window, textvariable=self.city_text,
                                font=("mincho", 15, "italic"),
                                bg="white",fg='#15317E',
                                bd=1, highlightthickness=1)
                                
        self.city_entry.place(x=65, y=64, width=305, height=31)
        self.city_entry.insert(0, " Enter city name:")
        self.city_entry.bind("<Button-1>", self.entry_clear)

        # Search Button#
        self.search_icon = Image.open("icons/search_icon.png")
        self.search_icon = self.search_icon.resize((26, 26), Image.ANTIALIAS)
        self.search_icon = ImageTk.PhotoImage(self.search_icon)

        search_btn = Button(self.window, cursor="hand2",
                            image=self.search_icon, bg="#15317E", bd=0,
                            activebackground="#15317E",
                            command=self.search).place(x=390, y=63, height=33, width=33)

        # Sign Label#
        sign_button = Button(self.window, anchor=CENTER,
                        relief=RAISED,
                        text="About Miracle Team.",
                        bg="#15317E", fg="#FFFFFF",
                        pady=4, command= self.openNewWindow2).pack(side=BOTTOM, fill=X)

        # Search History#
        Search_Page = Button(self.window,
                             anchor=CENTER,
                             text="Search History",
                             relief=RAISED, bd=3,
                             bg="#15317E",
                             fg="#FFFFFF",
                             pady=2,
                             command=self.openNewWindow).pack(side=BOTTOM, fill=X)

        self.location_lbl = Label(self.window, text="", font=('mincho', 20, "bold"),fg='#15317E', bg="white")
        self.location_lbl.place(x=0, y=100, relwidth=1, height=35)

        self.time_lbl = Label(self.window, text="",fg='#15317E', bg="white", font=("SimSun", 14))
        self.time_lbl.place(x=0, y=135, relwidth=1, height=20)

        self.img = PhotoImage(file="")
        self.image_lbl = Label(self.window, image=self.img, bg="white")
        self.image_lbl.place(x=0, y=160, relwidth=1, height=150)

        self.weather_lbl = Label(self.window, text="",fg='#15317E', bg="white", font=("mincho", 15))
        self.weather_lbl.place(x=0, y=300, relwidth=1, height=25)

        self.temp_lbl = Label(self.window, text="",fg='#15317E', bg="white", font=("SimSun-ExtB", 22))
        self.temp_lbl.place(x=0, y=340, relwidth=1, height=25)

        self.detail_btn = Button(self.window,cursor="hand2" ,text="",  width= 15, height= 7,
                                bg= "white", fg= "black", bd= 0, relief=RAISED, activebackground="white", 
                                font=("mincho", 13) , command= self.show_hide_detail)
        self.detail_btn.place(x=0, y=390, relwidth=1, height=20)
        
        self.sunrise_lbl = Label(self.window, text="",fg='#15317E', bg="white", font=("mincho", 13))
        self.sunset_lbl = Label(self.window, text="",fg='#15317E', bg="white", font=("mincho", 13))
        self.temp_max_lbl = Label(self.window, text="",fg='#15317E', bg="white", font=("mincho", 13))
        self.temp_min_lbl = Label(self.window, text="",fg='#15317E', bg="white", font=("mincho", 13))
    #Search history window
    def openNewWindow(self):
        self.new_window = Toplevel(self.window)
        self.new_window.title("Search History")
        self.new_window.geometry("600x600+100+150")
        self.new_window.configure(bg="white", padx=10, pady=10)
        self.new_window.resizable(False, False)
        self.text = StringVar()
        result_list = funcs.Show_search_history()
        print(result_list)
        s = ''
        for x in result_list:
            s += (x)
        self.text.set(s)
        
        Empty = "Database is Empty! +_+"
        if len(self.text.get()) == 0:
            self.text.set(Empty)
            print("--- All Data Erased! ---\n")


        Label2 = Label(self.new_window,
                       textvariable=self.text,
                       fg="white", bg='#15317E', relief=RAISED,
                       height=22, width=55, bd=3, font=('mincho', 13)).pack(expand=True)
        
        Button(self.new_window, anchor=CENTER,
               relief=RAISED,
               text="Delete Search Results",
               bg="#15317E", fg="#FFFFFF", bd=3,
               pady=4, command=lambda: [funcs.Erase_data(),
                                        self.new_window.destroy()]).pack(side=BOTTOM, fill=X)
    #Team members 
    def openNewWindow2(self): 
        self.new_window2 = Toplevel(self.window)
        self.new_window2.title("About Miracle Team")
        self.new_window2.geometry("400x200")
        self.new_window2.configure(bg="white", padx=10, pady=10)
        self.new_window2.resizable(False, False)  

        Label(self.new_window2,
              text="Miracle Team Members:\n"
                   "   1- Behrad Azimi (GitHub ID: behradiy)\n"
                   "   2- Amir Norani (GitHub ID: LogicalErr)\n"
                   "   3- Komeil Osali (GitHub ID: komeilosali)",
              font=("mincho", 13),
              fg="white", bg='#15317E',
              height=8, width=45,
              bd=2, relief=RIDGE, justify=LEFT, anchor=NW,
              ).pack(expand=False)

        Label(self.new_window2,
              text="Spring 2021-1400 / version 1.9.2.1",
              font=("italic", 10),
              fg="white", bg='#15317E',
              height=3, width=55,bd=2,
              relief=RIDGE,justify=CENTER
              ).pack(expand=False)                                     

    def show_hide_detail(self):
        
        weather_app.window.geometry("450x600+100+80")
        
        # Show details
        self.sunrise_lbl.place(x=0, y=430, relwidth=1, height=20)
        self.sunset_lbl.place(x=0, y=450, relwidth=1, height=20)
        self.temp_max_lbl.place(x=0, y=480, relwidth=1, height=20)
        self.temp_min_lbl.place(x=0, y=500, relwidth=1, height=20)


        if weather_app.sunrise_lbl["text"] == "":
            if weather:
                self.sunrise_lbl["text"] = "Sunrise: {} am".format(datetime.utcfromtimestamp(weather[8] + int(weather[7])).strftime('%c')[11:16])
                self.sunset_lbl["text"] = "Sunset: {} pm".format(datetime.utcfromtimestamp(weather[9] + int(weather[7] - 43200)).strftime('%c')[11:16])
                self.temp_min_lbl["text"] = "Low temperature: {:.2f}°C, {:.2f}°F".format(int(weather[10]) - 273.15, ( int(weather[10])-273.15 )*9/5 +32 )
                self.temp_max_lbl["text"] = "High temperature: {:.2f}°C, {:.2f}°F".format(int(weather[11]) - 273.15, ( int(weather[11])-273.15 )*9/5 +32 )
        else:
            # Hide details
            self.sunrise_lbl['text'] = ""
            self.sunset_lbl["text"] = ""
            self.temp_min_lbl["text"] = ""
            self.temp_max_lbl["text"] = ""
            self.sunrise_lbl.place(relwidth=0, height=0)
            self.sunset_lbl.place(relwidth=0, height=0)
            self.temp_max_lbl.place(relwidth=0, height=0)
            self.temp_min_lbl.place(relwidth=0, height=0)
            


            weather_app.window.geometry("450x500+100+80")



    def entry_clear(self, event):
        self.city_entry.delete(0, END)

    def search(self):

        city = self.city_text.get()
        global weather
        weather = get_weather(city)
        # weather = (city,country, temp_celcius, temp_fahrenheit, icons, weather, description_weather)
        if weather:

            self.city_entry.delete(0, END)
            self.city_entry.insert(0, f'Search for {city.title()} weather:')
            
            self.detail_btn["text"] = "Show/hide more details"
            self.location_lbl["text"] = "{}, {}".format(weather[0], weather[1])
            self.temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
            self.weather_lbl['text'] = "{}, {}".format(weather[5], weather[6])
            self.img['file'] = "icons/{}.png".format(weather[4])
            
            self.sunrise_lbl["text"] = ""
            self.sunset_lbl["text"] = ""
            self.temp_min_lbl["text"] = ""
            self.temp_max_lbl["text"] = ""

            while True:
                self.time_lbl['text'] = funcs.utc_con(int(weather[7]))
                window.update_idletasks()
                window.update()
                time.sleep(0.01)



        else:
            messagebox.showerror("Error", "Can't find city \"{}\"".format(city))


window = Tk()
window.iconphoto(False, PhotoImage(file="icons/icon_1.png"))
weather_app = MyWeatherApp(window)
window.resizable(False,False)
window.mainloop()
