from datetime import datetime
from configparser import ConfigParser
import sqlite3

config_file= 'config.ini'
config= ConfigParser()
config.read(config_file)

def utc_con(offset):
    l = str(datetime.utcnow())

    Hour = int(str(l[11] + l[12]))
    Minu = int(str(l[14] + l[15]))
    Second = int(str(l[17] + l[18]))
    Sec = Hour * 3600 + Minu * 60 + Second + offset

    NewHour = int(Sec / 3600)  # saate jadid
    if NewHour >= 24:
        NewHour = NewHour - 24
    NewMinu = Sec % 3600
    NewMinu = int(NewMinu / 60)  # daghigheye jadid
    NewSecond = Sec % 3600 - NewMinu * 60

    if NewSecond < 10 and NewMinu < 10 and NewHour < 10:
        final = "0{}:0{}:0{}"
    elif NewSecond < 10 and NewMinu < 10 and NewHour > 10:
        final = "{}:0{}:0{}"
    elif NewSecond < 10 and NewMinu > 10 and NewHour < 10:
        final = "0{}:{}:0{}"
    elif NewSecond < 10 and NewMinu > 10 and NewHour > 10:
        final = "{}:{}:0{}"
    elif NewSecond > 10 and NewMinu < 10 and NewHour < 10:
        final = "0{}:0{}:{}"
    elif NewSecond > 10 and NewMinu < 10 and NewHour > 10:
        final = "{}:0{}:{}"
    elif NewSecond > 10 and NewMinu > 10 and NewHour < 10:
        final = "0{}:{}:{}"
    else:
        final = "{}:{}:{}"

    return (final.format(NewHour, NewMinu, NewSecond))




def Data_Base(list):
    conn = sqlite3.connect('WEATHER.db')
    conn.execute(f"INSERT INTO history_search VALUES ('{list[0]}', '{list[1]}', {round(list[2], 2)}, {round(list[3], 2)}, '{list[4]}', '{utc_con(list[5])}');")
    print("--- Data was successfully deployed to DataBase. ---")
    conn.commit()
    conn.close()

def Show_search_history():
    list = []
    conn = sqlite3.connect('WEATHER.db')
    cursor = conn.execute("SELECT city, country, temp_celcius, temp_fahrenheit, weather, time FROM history_search;")
    rows = cursor.fetchall()
    for row in rows:
        print('city = ', row[0], end=" ")
        print('country = ', row[1], end=" ")
        print('temp_celcius = ', row[2], end=" ")
        print('temp_fahrenheit = ', row[3], end=" ")
        print('weather = ', row[4], end=" ")
        print('time = ', row[5], end=" ")
        list.append("{}\n".format(row))

    conn.commit()
    conn.close()
    return list




def Erase_data():
    conn = sqlite3.connect('WEATHER.db')
    conn.execute('DELETE FROM history_search;')
    conn.commit()
    conn.close()
    print("--- Deta Erased Successfully! ---\n")
