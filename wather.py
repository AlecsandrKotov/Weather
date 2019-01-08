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
# encoding: utf-8
from threading import Timer
from datetime import datetime, date, time
import time
from tkinter import messagebox
from random import uniform
from pyperclip import copy, paste

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
temp_time = 'Текущее время ' + datetime.now().strftime('%H:%M:%S')
after_id2 = ''


def time_tick():
    global temp_time, after_id
    after_id2 = root.after(1000, time_tick)
    lable1.configure(text=str(temp_time))
    temp_time = 'Текущее время ' + datetime.now().strftime('%H:%M:%S')

    return temp_time


# Копируем ссылку на файл для vMix ---------------------------------------------------------------------------------------
def copy_url_file_vmix():
    if os.path.exists(os.getcwd() + '\\wather.csv'):
        # print ("Файл найден")
        fil_vmix = os.getcwd() + '\\wather.csv'
        copy(fil_vmix)
    else:
        fil_vmix = 'Ссылка отсутствует'
        copy(fil_vmix)


# -----------------------------------------------------------------------------------------------------------------------
# Текущее время----------------------------------------------------------------------------------------------------------
temp = 180
after_id = ''


# Функция отсчета на основе случайного числа в диапозоне от 60 до 180
def tick():
    global temp, after_id, i
    after_id = root.after(1000, tick)
    # label1.configure(text=str(temp))
    temp -= 1
    if temp == 0:
        random_number()
        time_second()
        main()


def time_second():
    global update_text, tm
    tm = datetime.now().strftime('%H:%M:%S')
    update_text = 'Информация обнавлена - ' + str(tm)
    return update_text


# функция остановки таймера
def stop():
    print(temp)
    root.after_cancel(after_id)
    # label1.configure(text='0')
    random_number()


# функция генерации случайного числа
def random_number():
    global temp, random_update_text
    temp = int(uniform(60, 180))
    print(temp)
    # random_update_text = 'Следующее обновление через - ' + str(temp) + ' секунд'

    if var1.get() == 0:
        random_update_text = 'Следующее обновление через - ' + str(temp) + ' секунд'
    if var1.get() == 1:
        random_update_text = 'Следующее обновление через - 0 секунд'


def start():
    global temp
    main()


# tick()

# функция проверки установленной галочки	и запуск или остановка таймера
def check1_click():
    global random_update_text
    if var1.get() == 0:
        print('Галка есть')
        random_update_text = 'Следующее обновление через - ' + str(temp) + ' секунд'
        main()
        tick()
    if var1.get() == 1:
        random_update_text = 'Следующее обновление через - 0 секунд'
        print('Галки нет')
        stop()
        main()


# -----------------------------------------------------------------------------------------------------------------------


def main():
    # random_time() #Получаем случайное число в пределе от 60 до 180 для обновления данных

    global update_text
    url_site = Entry1.get().strip()
    # print(url_site)
    try:
        html = requests.get(url_site)
        # print (html.status_code) #200 если все ОК или ConnectionError  -  UnboundLocalError
        html_code = html.content  # Код страницы в формате HTML
        soup = BeautifulSoup(html_code, 'lxml')  # Код страницы в формате HTML помещаем в обьект SOUP
    except Exception:
        status = 'Ошибка подключения, проверьте подключение к интернет и доступность сайта '
        print(status)
    # sys.exit() #Остановка выполнения кода

    try:
        global now
        now = soup.find('div', class_='temp').text  # Сейчас температура
        # now = soup.find('div', class_='temp fact__temp').text #Сейчас температура
        print(now_text + now)
    except Exception:
        now = text_error
        print(now)

    try:
        global now_txt
        now_txt = soup.find('div', class_='link__condition day-anchor i-bem').text  # Статус текстом
        print(now_txt)
    except Exception:
        now_txt = text_error
        print(now_txt)

    try:
        global wind

        wind0 = soup.find('div', class_='fact__props')  # Ветер
        wind1 = wind0.find('dl', class_='term term_orient_v fact__wind-speed')
        wind2 = wind1.find('dd', class_='term__value').text
        wind = wind2
        print(wind_text + wind)

    # wind_full = str(wind) + wind_text_par + direction

    except Exception:
        wind = text_error
        print(wind)

    try:
        global pressure
        pressure0 = soup.find('div', class_='fact__props')  # Давление
        pressure1 = pressure0.find('dl', class_='term term_orient_v fact__pressure')
        pressure = pressure1.find('dd', class_='term__value').text
        print(pressure_text + pressure)  # соединяем текст и единицы измерения

    except Exception:
        pressure = text_error
        print(pressure)

    try:
        global humidity2
        humidity0 = soup.find('div', class_='fact__props')  # Влажность
        humidity1 = humidity0.find('dl', class_='term term_orient_v fact__humidity')
        humidity2 = humidity1.find('dd', class_='term__value').text
        print(humidity2_text + humidity2)
    except Exception:
        humidity2 = text_error
        print(humidity2)

    try:
        global feel2
        feel0 = soup.find('div', class_='fact__temp-wrap')  # Ощущается как
        feel1 = feel0.find('dl', class_='term term_orient_h fact__feels-like')
        feel2 = feel1.find('dd', class_='term__value').text
        print(feel2_text + feel2)
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
        print(yesterday2_text + yesterday2)

    except Exception:
        yesterday2 = text_error

    try:
        global nowcast
        nowcast = soup.find('p', class_='maps-widget-fact__title').text  # Ближайший прогноз
        # nowcast = soup.find('div', class_='nowcast-alert__text').text #Ближайший прогноз
        print(nowcast)
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
                    print(img)
            else:
                # print('Ночь')
                # Если ночь то проверяем существование файла в папки "night"
                img_url = os.getcwd() + '\\img\\night\\' + img_find + '.png'
                if os.path.exists(img_url) == 1:
                    img = img_url  # ссылка на файл
                    print(img)



        else:
            print('Файл НЕсуществует')
    except Exception:
        img = text_error

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
    print(file_path_text)
    # -------------------------------------------------------------------------------------------------

    # заполняем поля формы с данными ---------------------------------------------------------------------------------------
    # Удаляем список строк из ListBox
    lis1.delete(0, lis1.size())
    # Выводим полученную ирформацию
    list1 = [now_text + now, now_txt, wind_text + wind, pressure_text + pressure, humidity2_text + humidity2,
             feel2_text + feel2, yesterday2_text + yesterday2, nowcast, img, update_separator, time_second(),
             random_update_text, update_separator, file_path_text]
    for i in list1:
        lis1.insert(END, i)


# Графический интерфейс --------------------------------------------------------------------
root = Tk()
root.title('Wather для vMix - ver02')
root.minsize(620, 430)
root.iconbitmap('img\\myicon.ico')

root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

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

l3 = ttk.LabelFrame(root, text='Настройка обновления')
l3.grid(row=2, column=0, padx=10, pady=5, sticky='enws')

var1 = IntVar()
var1.set(1)  # присваиваем значение переменной 1- включено   0-выключено
check1 = ttk.Checkbutton(l3, text=u'Случайное обновление от 1 до 3 минут', variable=var1, onvalue=0, offvalue=1,
                         command=check1_click)
# check1.grid(row=2, column=0, padx=10, pady=10, sticky='enws')
check1.pack(side=LEFT, padx=5, pady=5)

lable1 = ttk.Label(l3, text='Текущее время ' + datetime.now().strftime('%H:%M:%S'), font="Arial 10", justify=RIGHT)
lable1.pack(side=RIGHT, padx=5, pady=5)

b_vmix = ttk.Button(root, text='Скопировать путь к файлу "wather.csv" в буфер обмена', command=copy_url_file_vmix)
b_vmix.grid(row=3, column=0, padx=10, pady=5, sticky='enws')


def on_closing():
    if messagebox.askokcancel("Закрыть", "Вы действительно хоите закрыть программу?"):
        root.destroy()
        root.quit()


root.protocol("WM_DELETE_WINDOW", on_closing)

time_tick()  # Текущее время
random_number()  # функция генерации случайного числа

root.mainloop()

if __name__ == '__main__':
    pass
