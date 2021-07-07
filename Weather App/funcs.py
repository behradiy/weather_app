from datetime import datetime
import mysql.connector
from configparser import ConfigParser

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
    
    cnx= mysql.connector.connect(user = config['db']['user'],
                                password = config['db']['pass'],
                                port = config['db']['port'],
                                host = config['db']['host'],
                                database = config['db']['dbname']) 
                            
    cursor = cnx.cursor()

    cursor.execute('INSERT INTO {} VALUES(\'{}\', \'{}\', \'{}°C\' ,\'{}°F\', \'{}\', \'{}\')'.format(config['db']['tbname'],
                                                                                                        list[0],
                                                                                                        list[1],
                                                                                                        int(list[2]),
                                                                                                        int(list[3]),
                                                                                                        list[4],
                                                                                                        utc_con(list[5])))

    print("--- Data was successfully deployed to DataBase. ---")

    cnx.commit()
    cursor.close()
    cnx.close()

def Show_search_history():
    list = []
    cnx = mysql.connector.connect(user = config['db']['user'],
                                password = config['db']['pass'],
                                port = config['db']['port'],
                                host = config['db']['host'],
                                database = config['db']['dbname'])

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM weather;')
    for x in cursor.fetchall():
        list.append("{}\n".format(x))
        print(x)
        print('\n')

    cnx.commit()
    cursor.close()
    cnx.close()
    return list

def Erase_data():
    cnx = mysql.connector.connect(user = config['db']['user'],
                                password = config['db']['pass'],
                                port = config['db']['port'],
                                host = config['db']['host'],
                                database = config['db']['dbname'])  
                                
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM weather;')
    cnx.commit()
    cursor.close()
    cnx.close()
    print("--- Deta Erased Successfully! ---\n")
