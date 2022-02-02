from cgi import print_form
import csv
from datetime import timedelta
from datetime import datetime
from traceback import print_tb
from time import gmtime
from time import strftime

nieprawidlowa_dana = "Nieprawidlowa dana wprowadzona przez badacza"
niewystarczajaca_ilosc_danych = "Niewystarczajaca ilosc danych do obliczenia"
numer_przystanku = []
numer_lini = []
numer_pojazdu = []
data = []
godzina_planowa_z_rozkladu = []
godzina_faktycznego_przyjazdu = []
godzina_faktycznego_odjazdu = []
opoznienia_przyjazdu = []
czas_pojazdu_na_przystanku = []

def read_data_from_csv(filecsv):
    with open(filecsv, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            #print(row['numer_przystanku'])
             #print(row['numer_przystanku'].isdigit())
            numer_przystanku.append(row['numer_przystanku'])
            numer_lini.append(row['numer_lini'])
            numer_pojazdu.append(row['numer_pojazdu'])
            data.append(row['data'])
            godzina_planowa_z_rozkladu.append(row['godzina_planowa_z_rozkladu'])
            godzina_faktycznego_przyjazdu.append(row['godzina_faktycznego_przyjazdu'])
            godzina_faktycznego_odjazdu.append(row['godzina_faktycznego_odjazdu'])

    for i in range(len(numer_przystanku)):
        opoznienia_przyjazdu.append(0)
        czas_pojazdu_na_przystanku.append(0)


def check_the_number(list):
    for i in range(len(list)):
        if not list[i].isdigit():
            list[i] = nieprawidlowa_dana

def check_the_date(list):
    for i in range(len(list)):
        if list[i].find('.') == -1:    
            list[i] = nieprawidlowa_dana

def check_the_hour(list):       
    for i in range(len(list)):
        if list[i].find(":") == -1:
            list[i] = nieprawidlowa_dana

def check_all_data():
    check_the_number(numer_przystanku)
    check_the_number(numer_lini)
    check_the_number(numer_pojazdu)
    check_the_date(data)
    check_the_hour(godzina_planowa_z_rozkladu)
    check_the_hour(godzina_faktycznego_przyjazdu)
    check_the_hour(godzina_faktycznego_odjazdu)

def conversion_hour_to_second(hour):
    return hour*3600

def conversion_minute_to_second(minute):
    return minute*60;        

def calculate_time_of_delay_of_arrival(scheduled_hour, time_of_actual_arrival):
    for i in range(len(scheduled_hour)):
        if not scheduled_hour[i] == nieprawidlowa_dana and not time_of_actual_arrival[i] == nieprawidlowa_dana:
            index_of_found_colo = str(scheduled_hour[i]).find(":")
            minute_scheduled = str(scheduled_hour[i])[index_of_found_colo+1:len(scheduled_hour[i])]  
            hour_scheduled = str(scheduled_hour[i])[0:index_of_found_colo] 
            scheduled_in_second = int(conversion_hour_to_second(int(hour_scheduled))) + int(conversion_minute_to_second(int(minute_scheduled)))
            index_of_found_colo = str(time_of_actual_arrival[i]).find(":")
            minute_arrival = str(time_of_actual_arrival[i])[index_of_found_colo+1:len(time_of_actual_arrival[i])]  
            hour_arrival = str(time_of_actual_arrival[i])[0:index_of_found_colo] 
            arrival_in_second = int(conversion_hour_to_second(int(hour_arrival))) + int(conversion_minute_to_second(int(minute_arrival)))
            delay_in_second = arrival_in_second - scheduled_in_second
            if delay_in_second < 0:
                opoznienia_przyjazdu[i] = "00:00"
            else:                
                opoznienia_przyjazdu[i] = strftime("%H:%M", gmtime(delay_in_second))
        else:
            opoznienia_przyjazdu[i] = niewystarczajaca_ilosc_danych

def calculate_time_of_being_at_the_vehicle_stop(time_of_actual_arrival, time_of_actual_departure):
    for i in range(len(time_of_actual_arrival)):
        if not time_of_actual_arrival[i] == nieprawidlowa_dana and not time_of_actual_departure[i] == nieprawidlowa_dana:
            index_of_found_colo = str(time_of_actual_arrival[i]).find(":")
            minute_arrival = str(time_of_actual_arrival[i])[index_of_found_colo+1:len(time_of_actual_arrival[i])]  
            hour_arrival = str(time_of_actual_arrival[i])[0:index_of_found_colo] 
            arrival_in_second = int(conversion_hour_to_second(int(hour_arrival))) + int(conversion_minute_to_second(int(minute_arrival)))
            index_of_found_colo = str(time_of_actual_departure[i]).find(":")
            minute_departure = str(time_of_actual_departure[i])[index_of_found_colo+1:len(time_of_actual_departure[i])]  
            hour_departure = str(time_of_actual_departure[i])[0:index_of_found_colo] 
            departure_in_second = int(conversion_hour_to_second(int(hour_departure))) + int(conversion_minute_to_second(int(minute_departure)))
            down_time_in_second = departure_in_second - arrival_in_second
            czas_pojazdu_na_przystanku[i] = strftime("%H:%M", gmtime(down_time_in_second))
        else:
            czas_pojazdu_na_przystanku[i] = niewystarczajaca_ilosc_danych

def save_data_to_csv(csvFile):
        header = ['numer_przystanku','numer_lini','numer_pojazdu','data','godzina_planowa_z_rozkladu','godzina_faktycznego_przyjazdu',
        'godzina_faktycznego_odjazdu','opoznienia_przyjazdu', 'czas_pojazdu_na_przystanku']    

        with open(csvFile, 'w', newline='') as csvFile:   
            writer = csv.writer(csvFile)
            writer.writerow(header)
            for i in range(len(numer_przystanku)):
                    writer.writerow([numer_przystanku[i],numer_lini[i],
                   numer_pojazdu[i],data[i],godzina_planowa_z_rozkladu[i],
                    godzina_faktycznego_przyjazdu[i],godzina_faktycznego_odjazdu[i],opoznienia_przyjazdu[i],czas_pojazdu_na_przystanku[i]])
    
        return None            
           
           
read_data_from_csv('Punktulaność-komunikacji-miejskiej.csv') 
check_all_data()
calculate_time_of_being_at_the_vehicle_stop(godzina_faktycznego_przyjazdu, godzina_faktycznego_odjazdu)
calculate_time_of_delay_of_arrival(godzina_planowa_z_rozkladu, godzina_faktycznego_przyjazdu)
save_data_to_csv('Punktulaność-komunikacji-miejskiej-po-obliczeniach.csv')
       
 