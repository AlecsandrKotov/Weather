# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import os.path
import datetime
import csv
import sys
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from threading import Timer
from datetime import datetime, date, time, timedelta
import time
from tkinter import messagebox
from random import uniform
from pyperclip import copy, paste
import threading

# Компиляция
text_error = '--'
# ---------------------------------------------------------------------
now_text = 'Сейчас '  # текст перед выводом грудусов "Сейчас:"
now = ''  # градусы сейчас
# ---------------------------------------------------------------------
now_txt = ''  # Статус пример: "Облачно с проясненими"
# ---------------------------------------------------------------------
wind_text = 'Ветер '  # текст перед выводом цифр
wind = ''  # Ветер цифры или текст
wind_text_par = ' м/с,'  # Единицы измерения ветра "м/с"
direction = ''  # Направление ветра
# ---------------------------------------------------------------------
pressure_text = 'Давление '  # текст перед выводом цифр
pressure = ''  # Давление в цифрах
# ---------------------------------------------------------------------
humidity2 = ''  # Влажность в цифрах
humidity2_text = 'Влажность '  # текст перед выводом цифр
# ---------------------------------------------------------------------
feel2_text = 'Ощущается как '  # текст перед выводом цифр
feel2 = ''  # Ощущается как в цифрах
# ---------------------------------------------------------------------
yesterday0 = ''
yesterday1 = ''
yesterday2_text = 'Вчера в это время '  # текст перед выводом цифр
yesterday2 = ''  # Вчера в это же время в цифрах
# ---------------------------------------------------------------------
nowcast = ''  # Ближайший прогноз
# ---------------------------------------------------------------------
img = ''  # ссылка на картинку погоды

update_separator = '-----------------------------------------------------------------'

# Вывод текущего времени вывод в lable1 --------------------------------------------------------------
#temp_time = 'Текущее время ' + datetime.now().strftime('%H:%M:%S')
temp_time = datetime.now().strftime('%H:%M:%S')
after_id2 = ''

# Отдельный поток - обёртка для последующих функций
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper

@thread
def time_tick():
    global temp_time, after_id
    after_id2 = root.after(1000, time_tick)

    if var1.get() == 1:
        lable1.configure(text=str(temp_time))
        temp_time = datetime.now().strftime('%H:%M:%S')
        return temp_time

    
    if var1.get() == 0:
        mytime = datetime.now()
        mytimer = datetime.now() +  timedelta(seconds=temp)
        count = mytimer.strftime('%H:%M:%S')
        result_timer = mytimer - mytime
        #print (result_timer)
        lable1.configure(text=str(result_timer))
        return result_timer


# Копируем ссылку на файл для vMix ---------------------------------------------------------------------------------------
@thread
def copy_url_file_vmix():
    if os.path.exists(os.getcwd() + '\\wather.csv'):
        # print ("Файл найден")
        fil_vmix = os.getcwd() + '\\wather.csv'
        copy(fil_vmix)
    else:
        fil_vmix = 'Ссылка отсутствует'
        copy(fil_vmix)

# Текущее время----------------------------------------------------------------------------------------------------------
temp = 180
after_id = ''


# Функция отсчета на основе случайного числа в диапозоне от 60 до 180
@thread
def tick():
    global temp, after_id, i
    after_id = root.after(1000, tick)
    # label1.configure(text=str(temp))
    temp -= 1
    if temp == 0:
        random_number()
        time_second()
        main()

#@thread
def time_second():
    global update_text, tm
    tm = datetime.now().strftime('%H:%M:%S')
    update_text = 'Информация обнавлена - ' + str(tm)
    return update_text


# функция остановки таймера
@thread
def stop():
    #print("таймер" + str(temp))
    root.after_cancel(after_id)
    # label1.configure(text='0')
    random_number()


# функция генерации случайного числа
def random_number():
    global temp, random_update_text
    temp = int(uniform(60, 180))
    #print("таймер" + str(temp))
    # random_update_text = 'Следующее обновление через - ' + str(temp) + ' секунд'

    x = datetime.now() + timedelta(seconds=temp)
    mycount = x.strftime('%H:%M:%S')


    if var1.get() == 0:
        random_update_text = 'Следующее обновление в - ' + str(mycount)
    if var1.get() == 1:
        random_update_text = 'Автообновление отключено'


@thread
def start():
    global temp
    main()


# функция проверки установленной галочки и запуск или остановка таймера
@thread
def check1_click():
    global random_update_text
    x = datetime.now() +timedelta(seconds=temp)
    mycount = x.strftime('%H:%M:%S')



    if var1.get() == 0:
        #print('Галка есть')
        random_update_text = 'Следующее обновление в - ' + str(mycount)
        main()
        tick()
    if var1.get() == 1:
        random_update_text = 'Автообновление отключено'
        #print('Галки нет')
        stop()
        main()
# -----------------------------------------------------------------------------------------------------------------------
@thread
def main():
    global update_text
    url_site = Entry1.get().strip()
    try:
        user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) ' 'Gecko/20100101 Firefox/64.0') 
        html = requests.get(url_site, headers={'User-Agent':user_agent})
        #print (html.status_code) #200 если все ОК или ConnectionError  -  UnboundLocalError
        html_code = html.content  # Код страницы в формате HTML
        soup = BeautifulSoup(html_code, 'lxml')  # Код страницы в формате HTML помещаем в обьект SOUP
    except Exception:
        status = 'Ошибка подключения, проверьте подключение к интернет и доступность сайта '
        print(status)

    try:
        global now
        now = soup.find('div', class_='temp').text  # Сейчас температура
    except Exception:
        now = text_error
        print(now)

    try:
        global now_txt
        now_txt = soup.find('div', class_="link__condition day-anchor i-bem").text  # Статус текстом
    except Exception:
        now_txt = text_error
        print(now_txt)

    try:
        global wind

        wind0 = soup.find('div', class_='fact__props')  # Ветер
        wind1 = wind0.find('dl', class_='term term_orient_v fact__wind-speed')
        wind2 = wind1.find('dd', class_='term__value').text
        wind = wind2

    except Exception:
        wind = text_error
        print(wind)

    try:
        global pressure
        pressure0 = soup.find('div', class_='fact__props')  # Давление
        pressure1 = pressure0.find('dl', class_='term term_orient_v fact__pressure')
        pressure = pressure1.find('dd', class_='term__value').text
        #print(pressure_text + pressure)  # соединяем текст и единицы измерения

    except Exception:
        pressure = text_error
        print(pressure)

    try:
        global humidity2
        humidity0 = soup.find('div', class_='fact__props')  # Влажность
        humidity1 = humidity0.find('dl', class_='term term_orient_v fact__humidity')
        humidity2 = humidity1.find('dd', class_='term__value').text
        #print(humidity2_text + humidity2)
    except Exception:
        humidity2 = text_error
        print(humidity2)

    try:
        global feel2
        feel0 = soup.find('div', class_='fact__temp-wrap')  # Ощущается как
        feel1 = feel0.find('dl', class_='term term_orient_h fact__feels-like')
        feel2 = feel1.find('dd', class_='term__value').text
        #print(feel2_text + feel2)
    except Exception:
        feel2 = text_error
        print(feel2)

    try:
        global yesterday2
        # yesterday0 = soup.find('div', class_='fact__temp-wrap') #Вчера в это время
        # yesterday1 = yesterday0.find('dl', class_='term term_orient_h fact__yesterday')
        # yesterday2 = yesterday1.find('dd', class_='term__value').text
        # print(yesterday2_text + yesterday2)
        yesterday0 = soup.find('dl', class_='term_size_wide')  # Вчера в это время
        yesterday2 = yesterday0.find('span', class_='temp__value').text
        #print(yesterday2_text + yesterday2)

    except Exception:
        yesterday2 = text_error

    try:
        global nowcast
        nowcast = soup.find('p', class_='maps-widget-fact__title').text  # Ближайший прогноз
        if nowcast == "Погода сейчас и прогноз — на картах":
            nowcast = "Нет данных"
        # nowcast = soup.find('div', class_='nowcast-alert__text').text #Ближайший прогноз
        #print(nowcast)
    except Exception:
        nowcast = text_error
        print(nowcast)

    try:
        global img
        # global img_sl
        # создаем словарь с статусом с сайта и названиями файлов (имя файла)
        img_sl = {'ясно': 'clear',
                  'малооблачно': 'partly-cloudy',
                  'облачно с прояснениями': 'cloudy',
                  'пасмурно': 'overcast',
                  'небольшой дождь': 'partly-cloudy-and-light-rain',
                  'дождь': 'partly-cloudy-and-rain',
                  'сильный дождь': 'overcast-and-rain',
                  'сильный дождь, гроза': 'overcast-thunderstorms-with-rain',
                  'небольшой дождь': 'cloudy-and-light-rain',
                  'дождь со снегом': 'overcast-and-wet-snow',
                  'снег': 'partly-cloudy-and-snow',
                  'снегопад': 'overcast-and-snow',
                  'небольшой снег': 'cloudy-and-light-snow'}
        # print (img_sl)

        # Конвертируем текст в нижний регистр
        now_txt_lower = now_txt.lower().strip()
        # Удаляем пробелы у значения имени файла в начале и конце
        img_find = img_sl[now_txt_lower].strip()
        img_foder = os.getcwd() + '\\img\\'

        # Проверка существования папки и вывод картинок в зависимости день это или ночь
        if os.path.exists(img_foder) == 1:
            now_t = datetime.now()
            a = now_t.hour  # время сейчас (часы)
            # print (a)

            if 6 <= a <= 20:
                # print('День')
                # Если день то проверяем существование файла в папки "day"
                img_url = os.getcwd() + '\\img\\day\\' + img_find + '.png'
                if os.path.exists(img_url) == 1:
                    img = img_url  # ссылка на файл
                    #print(img)
            else:
                # print('Ночь')
                # Если ночь то проверяем существование файла в папки "night"
                img_url = os.getcwd() + '\\img\\night\\' + img_find + '.png'
                if os.path.exists(img_url) == 1:
                    img = img_url  # ссылка на файл
                    #print(img)
        else:
            print('Файл НЕсуществует')
    except Exception:
        img = text_error


    print (now)
    print (now_txt)
    print (wind)
    print (pressure)
    print (humidity2)
    print (feel2)
    print (yesterday2)
    print (nowcast)     
    print (img)

    #сохранять в случае если все данные получены
    if var2.get() == 1:
        print ("галка стоит")
        if str(now) != str(text_error) and str(now_txt) != str(text_error) and str(wind) != str(text_error) and str(pressure) != str(text_error) and str(humidity2) != str(text_error) and str(feel2) != str(text_error) and str(yesterday2) != str(text_error) and str(nowcast) != str(text_error) and str(img) != str(text_error):
            global save
            save = "Все хорошо, файл сохранен."
            lable2.configure(text="ВСЕ ХОРОШО", foreground="white", background="green")
            with open('wather.csv', 'w', encoding='utf-8', newline='') as f:
                t = csv.writer(f)
                t.writerow([now_text, now])  # Градусы
                t.writerow([now_txt])  # Статус
                t.writerow([wind_text, wind])  # Ветер
                t.writerow([pressure_text, pressure])  # Давление
                t.writerow([humidity2_text, humidity2])  # Влажность
                t.writerow([feel2_text, feel2])  # Ощущается как
                t.writerow([yesterday2_text, yesterday2])  # вчера в это время
                t.writerow([nowcast])  # Блидайший прогноз
                t.writerow([img])  # Картинка 
        else:
            lable2.configure(text="ОШИБКА", foreground="white", background="red")
            save = "Ошибка получения данных, фай не сохранен!"

    #сохранять в любом случае       
    if var2.get() == 0:
        print ("галки нет")
        save = "Файл сохранен."
        lable2.configure(text="", foreground="white", background="white")
        with open('wather.csv', 'w', encoding='utf-8', newline='') as f:
            t = csv.writer(f)
            t.writerow([now_text, now])  # Градусы
            t.writerow([now_txt])  # Статус
            t.writerow([wind_text, wind])  # Ветер
            t.writerow([pressure_text, pressure])  # Давление
            t.writerow([humidity2_text, humidity2])  # Влажность
            t.writerow([feel2_text, feel2])  # Ощущается как
            t.writerow([yesterday2_text, yesterday2])  # вчера в это время
            t.writerow([nowcast])  # Блидайший прогноз
            t.writerow([img])  # Картинка 


    # Проверка существования файла для vMix (mycsv.csv)-------------------------------------------
    global file_path
    global file_path_text

    file_path = os.getcwd() + '\\wather.csv'
    file_path_text = 'путь к файлу для vMix - ' + file_path

    i = os.path.isfile(file_path)
    if not i:
        file_path_text = 'Файл для vMix отсутствует'

    else:
        file_path_text = 'Путь к файлу для vMix - ' + file_path
    # -------------------------------------------------------------------------------------------------

    # заполняем поля формы с данными ---------------------------------------------------------------------------------------
    # Удаляем список строк из ListBox
    lis1.delete(0, lis1.size())
    # Выводим полученную ирформацию
    list1 = [now_text + now, now_txt, wind_text + wind, pressure_text + pressure, humidity2_text + humidity2,
             feel2_text + feel2, yesterday2_text + yesterday2, nowcast, img, update_separator, time_second(),
             random_update_text, update_separator, save ] #, file_path_text
    for i in list1:
        lis1.insert(END, i)


# Графический интерфейс --------------------------------------------------------------------
root = Tk()
root.title('Wather для vMix - ver03')
root.minsize(620, 464)
root.iconbitmap('img\\myicon.ico')

l1 = ttk.LabelFrame(root, text='Введите URL страницы')
l1.grid(row=0, column=0, padx=5, pady=5, sticky='enws')

b1 = ttk.Button(l1, text='Обновить', command=start)
b1.pack(side=RIGHT, padx=5, pady=5)


# Вставляем текст из буфера
def paste_Entry1():
    Entry1.delete(0, 'end')
    a = paste()
    Entry1.insert(0, a)


# Очищаем элемент Entry1
def clear_Entry1():
    Entry1.delete(0, 'end')


def wather_moskow():
    Entry1.delete(0, 'end')
    Entry1.insert(0, 'https://yandex.ru/pogoda/moscow/')


def do_popup(event):
    # display the popup menu
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup.grab_release()


popup = Menu(root, tearoff=0)
popup.add_command(label="Погода в Москве", command=wather_moskow)
popup.add_separator()
popup.add_command(label="Вставить из буфера", command=paste_Entry1)
popup.add_separator()
popup.add_command(label="Удалить содержимое", command=clear_Entry1)

Entry1 = ttk.Entry(l1, width=70)
Entry1.pack(side=LEFT, fill=X, expand=1, padx=5, pady=5)
Entry1.insert(0, 'https://yandex.ru/pogoda/moscow')
Entry1.bind('<Button-3>', do_popup)
Entry1.focus_set()

l2 = ttk.LabelFrame(root, text='Результат')
l2.grid(row=1, column=0, padx=5, pady=5, sticky='enws')

lis1 = Listbox(l2)
lis1.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)

var1 = IntVar()
var1.set(1)  # присваиваем значение переменной 1- включено   0-выключено

var2 = IntVar()
var2.set(1)  # присваиваем значение переменной 1- включено   0-выключено

l5 = ttk.LabelFrame(root, text='Настройка обновления')
l5.grid(row=2, column=0, padx=10, pady=5, sticky='enws')

check1 = ttk.Checkbutton(l5, text=u'Автообновление чрез случайный диапозон (от 1 до 3 минуты)', variable=var1, onvalue=0, offvalue=1, command=check1_click)
check1.grid(row=4, column=0, padx=10, pady=5, sticky='enws')

#lable1 = ttk.Label(l5, text='Текущее время ' + datetime.now().strftime('%H:%M:%S'), font="Arial 10", justify=RIGHT, anchor = "e")
lable1 = ttk.Label(l5, text=datetime.now().strftime('%H:%M:%S'), font="Arial 14", justify=RIGHT, anchor = "e")
lable1.grid(row=4, column=1, padx=10, pady=5, sticky='e')

check2 = ttk.Checkbutton(l5, text=u'Отменить сохранение при отсутствии каки либо данных c источника', variable=var2, onvalue=1, offvalue=0, )
check2.grid(row=5, column=0, padx=10, pady=5, sticky='enws')

lable2 = ttk.Label(l5, text='', font="Arial 12", justify=RIGHT, anchor = "e", foreground="white")
lable2.grid(row=5, column=1, padx=10, pady=5, sticky='e')

b_vmix = ttk.Button(root, text='Скопировать путь к файлу "wather.csv" в буфер обмена', command=copy_url_file_vmix)
b_vmix.grid(row=6, column=0, padx=10, pady=5, sticky='enws')

l5.rowconfigure(1, weight=1)
l5.columnconfigure(0, weight=1)

def on_closing():
    if messagebox.askokcancel("Закрыть", "Вы действительно хоите закрыть программу?"):
        root.destroy()
        root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)

time_tick()  # Текущее время
random_number()  # функция генерации случайного числа

root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

root.mainloop()
