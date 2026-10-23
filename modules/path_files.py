#                                                                                 
#    PPPPPPPPPPPPPPPPP                           tttt         hhhhhhh             
#    P::::::::::::::::P                       ttt:::t         h:::::h             
#    P::::::PPPPPP:::::P                      t:::::t         h:::::h             
#    PP:::::P     P:::::P                     t:::::t         h:::::h             
#      P::::P     P:::::Paaaaaaaaaaaaa  ttttttt:::::ttttttt    h::::h hhhhh       
#      P::::P     P:::::Pa::::::::::::a t:::::::::::::::::t    h::::hh:::::hhh    
#      P::::PPPPPP:::::P aaaaaaaaa:::::at:::::::::::::::::t    h::::::::::::::hh  
#      P:::::::::::::PP           a::::atttttt:::::::tttttt    h:::::::hhh::::::h 
#      P::::PPPPPPPPP      aaaaaaa:::::a      t:::::t          h::::::h   h::::::h
#      P::::P            aa::::::::::::a      t:::::t          h:::::h     h:::::h
#      P::::P           a::::aaaa::::::a      t:::::t          h:::::h     h:::::h
#      P::::P          a::::a    a:::::a      t:::::t    tttttth:::::h     h:::::h
#    PP::::::PP        a::::a    a:::::a      t::::::tttt:::::th:::::h     h:::::h
#    P::::::::P        a:::::aaaa::::::a      tt::::::::::::::th:::::h     h:::::h
#    P::::::::P         a::::::::::aa:::a       tt:::::::::::tth:::::h     h:::::h
#    PPPPPPPPPP          aaaaaaaaaa  aaaa         ttttttttttt  hhhhhhh     hhhhhhh
#                                                                                 
# Module                                                                                                         

                              
import os
import re

import winreg
import configparser 

import tkinter as tk
from tkinter import filedialog





def get_steam_path() -> str | None:
    try:
        key_path = r"SOFTWARE\Wow6432Node\Valve\Steam"                                          #ключ к поиску корневой папки Steam 

        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:                        #чтение ключа реестра
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")                             #поиск корневой папки через переменную "InstallPath"

            return steam_path                                                                   #вывод пути
        
    except FileNotFoundError:                                                                   #на случай ошибки
        return None



def get_steam_nickname() -> str | None:
        try:        
            loginusers_path = os.path.join(get_steam_path(), "config", "loginusers.vdf")        #файл содержащий информацию 
            if not os.path.exists(loginusers_path):return "Unknown"                             #если файла нет, то и имени тоже


            with open(loginusers_path, 'r', encoding='utf-8') as file:data = file.read()        #открываем файл для чтения
            accounts = re.findall(r'"(\d{17})"\s*\{(.*?)\}', data, re.DOTALL)                   #парсинг структуры файла


            for steam_id, content in accounts:                                                      
                if re.search(r'"MostRecent"\s*"1"', content):                                   #поиск самого недавнего аккаунта
                    person_match = re.search(r'"PersonaName"\s*"(.+?)"', content)     

                    if person_match:                                                            #в случае находки
                        return person_match.group(1) if person_match.group(1) else "Unknown"    #вывод либо никнейма, либо ничего

 
                    break                                                                       #остановка цикла для экономии времени 
        except: return None                                                                     #на случай ошибки




def select_path_window(window_title:str = "Выберите папку, пожалуйста") -> str | None:
    try:
        root = tk.Tk()                                                                          #инициализация окна ткинтера
        root.withdraw()                                                                         #отрисовка окна ткинтера


        return filedialog.askdirectory(title = window_title)                                    #вывод выбранной директории
    except: return None



def read_ini_file(file_path:str, section:str, key:str) -> str | None:   
    try:
        config = configparser.ConfigParser()                                                    #инициализация парсера                    
        config.read(file_path, encoding='utf-8')                                                #чтение документа

        return config.get(section, key, fallback = None)                                        #вывод значение через ключ и секцию
    except: return None                                                                         #на случай ошибки



def write_ini_file(file_path:str, section:str, key:str, value:str) -> None:
    try:    
        config = configparser.ConfigParser()                                                    #инициализация парсера 
        config.read(file_path, encoding='utf-8')                                                #чтение документа

      
        config[section][key] = value                                                            #изменение существующего значение, или добавление нового
                                                                                      
        with open(file_path, 'w', encoding='utf-8') as f:                                       #применение изменений
            config.write(f)

    except: return None 



if __name__ == "__main__":
    print( get_steam_nickname() )

    #print( select_path_window() )
    #print( read_ini_file()      )
    #write_ini_file()