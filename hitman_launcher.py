#                                                                                                   
#                                                                                                   
#            CCCCCCCCCCCCC                                                       kkkkkkkk           
#         CCC::::::::::::C                                                       k::::::k           
#       CC:::::::::::::::C                                                       k::::::k           
#      C:::::CCCCCCCC::::C                                                       k::::::k           
#     C:::::C       CCCCCCrrrrr   rrrrrrrrr   aaaaaaaaaaaaa      cccccccccccccccc k:::::k    kkkkkkk
#    C:::::C              r::::rrr:::::::::r  a::::::::::::a   cc:::::::::::::::c k:::::k   k:::::k 
#    C:::::C              r:::::::::::::::::r aaaaaaaaa:::::a c:::::::::::::::::c k:::::k  k:::::k  
#    C:::::C              rr::::::rrrrr::::::r         a::::ac:::::::cccccc:::::c k:::::k k:::::k   
#    C:::::C               r:::::r     r:::::r  aaaaaaa:::::ac::::::c     ccccccc k::::::k:::::k    
#    C:::::C               r:::::r     rrrrrrraa::::::::::::ac:::::c              k:::::::::::k     
#    C:::::C               r:::::r           a::::aaaa::::::ac:::::c              k:::::::::::k     
#     C:::::C       CCCCCC r:::::r          a::::a    a:::::ac::::::c     ccccccc k::::::k:::::k    
#      C:::::CCCCCCCC::::C r:::::r          a::::a    a:::::ac:::::::cccccc:::::ck::::::k k:::::k   
#       CC:::::::::::::::C r:::::r          a:::::aaaa::::::a c:::::::::::::::::ck::::::k  k:::::k  
#         CCC::::::::::::C r:::::r           a::::::::::aa:::a cc:::::::::::::::ck::::::k   k:::::k 
#            CCCCCCCCCCCCC rrrrrrr            aaaaaaaaaa  aaaa   cccccccccccccccckkkkkkkk    kkkkkkk
#                                                                                                    
# made by - Wl13Proger9         
#       
# ..steamapps\common\HITMAN 3\Retail

                                                                                             
import re
import os
import sys

import time
import ctypes

import subprocess
import configparser 



phrases = {
    "en": {
            1: "File <PeacockPatcher.exe> not found! It’s possible that the antivirus deleted it.",
            2: "File <Start Server.cmd> not found! It’s possible that the antivirus deleted it.",
            3: "File <steamclient_loader_x64.exe> not found! It’s possible that the antivirus deleted it.",

            4: "Error with file: This file not found.",
        },

    "ru": {
            1: "Файл <PeacockPatcher.exe> не найден! Возможно его удалил антивирус.",
            2: "Файл <Start Server.cmd> не найден! Возможно его удалил антивирус.",
            3: "Файл <steamclient_loader_x64.exe> не найден! Возможно его удалил антивирус.",

            4: "Ошибка с файлом: Данный файл не найден.",
    }
}                                                                             # фразы для ошибок

lang              = "en"                                                      # язык
pid_collection    = {}                                                        # коллекция PID индефикаторов
ab_path           = os.getcwd()                                               # путь к директории обьекта


peacock_path      = os.path.join(ab_path, 'peacock', 'PeacockPatcher.exe')    # взломанный патчер Peacock
peacock_cmd_path  = os.path.join(ab_path, 'peacock', 'Start Server.cmd')      # взломанный сервер Peacock
peacock_node_path = os.path.join(ab_path, 'peacock', 'nodedist', 'node.exe')  # Nodejs Peacock

game_path         = os.path.join(ab_path, 'steamclient_loader_x64.exe')       # взломанный клиент игры
steam_game_path   = os.path.join(ab_path, 'HITMAN3.exe')                      # сама игра
launcher_settings = os.path.join(ab_path, 'launcher_settings')                # папка настроек лаунчера


DETACHED_PROCESS    = 0x00000008                                              # windows флаг для независимого запуска
CREATE_NO_WINDOW    = 0x08000000                                              # windows флаг для создания без окна консоли
CREATE_NEW_CONSOLE  = 0x10                                                    # windows флаг для создания нового окна консоли
                         
PID_INI_FNAME       = "PID_collections.ini"                                   # имя .ini файла с коллекцией PID
SETTINGS_INI_FNAME  = "launcher_settings.ini"                                 # имя .ini файла с настройками лаунчера

DEFAULT_AWAIT_TIME  = 0.3                                                     # задержка для работы скрипта (default = 0.3)
SILENT_MODE         = True                                                    # скрытый режим

startupinfo             = subprocess.STARTUPINFO()                            # информация об запускаемом окне
startupinfo.dwFlags    |= subprocess.STARTF_USESHOWWINDOW                     # добавление флага STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE                                  # скрытие окна с экрана



def show_error_message(message:str, title:str) -> None:                       # функция для окна ошибок
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)                 # само окно ошибок


def update_ini(file_path:str, section:str, key:str, value:str) -> None:       # функция для изменение ini файлов   
    config = configparser.ConfigParser()                                      # инициализация парсера 
    config.read(file_path, encoding='utf-8')                                  # чтение документа

    
    config[section][key] = value                                              # изменение существующего значение, или добавление нового  
    with open(file_path, 'w', encoding='utf-8') as f:                         # применение изменений
        config.write(f)


def get_procces_pid(process_name:str, procces_path:str) -> str:               # функция для взятия PID самой игры
    try:
        command = f"Get-Process -Name {process_name} | Where-Object {{ $_.Path -eq '{procces_path}' }} | Select-Object Id"

        result = subprocess.run(
            [ "powershell", "-Command", command ],                            # исполнение команды через Powershell
            capture_output = True,
            text           = True,
            encoding       = "cp866",
            creationflags  = CREATE_NO_WINDOW
        ).stdout

        #print(result)
        return re.findall(r'\d+', result)[0]                                  # парсинг данных вывода
    
    except Exception as error_message:                                        # на случай ошибки
        show_error_message(message = error_message,
                            title  = phrases[lang][4])
    

def startup() -> None:                                                        # функция для начала работы скрипта
    def _check_ini(file_path:str, section:str, key:str) -> bool | None:     # подфункция для чтения .ini  
        try:
            config = configparser.ConfigParser()                            # инициализация парсера                    
            config.read(file_path, encoding='utf-8')                        # чтение документа

            return config.getboolean(section, key, fallback = None)         # вывод значение через ключ и секцию
        except: return None                                                 # на случай ошибки


    global SILENT_MODE                                                        # для работы с данной переменной
    os.makedirs(launcher_settings, exist_ok=True)                             # создание папки настроек ланучера

    drawing_window =  _check_ini(                                             # узнать насчёт silent_mode
            file_path = os.path.join( launcher_settings, SETTINGS_INI_FNAME ),
            section   = "STARTUP",
            key       = "silent_mode" 
        )
    
    content = """[PID]                                                              
peacock=                                                                      
server= 
client= 
nodejs=

[GAME_PID]
steam_game=
"""                                                                           # содержимое коллекции PID
    

    with open(os.path.join( launcher_settings, PID_INI_FNAME ), "w") as f:    # создания списка PID
        f.write(content)
        f.close()

    if drawing_window == False: 
        SILENT_MODE = False



startup()                                                                     # начала алгоритма 
print(f"silent_mode: {SILENT_MODE}")                                          # вывод каков silent_mode


try:                                                                          # установка языка
    argv = sys.argv[1]                                                        # аргументы

    match argv:
        case "ru": lang = "ru"                                                # русский
        case "en": lang = "en"                                                # английский
        case    _: lang = "en"
                                                          
except:pass                                                                   # на случай если нет аргументов




try:                                                                          # :[ запуск патчера <PeacockPatcher.exe> ]:     
    if SILENT_MODE:                                                           # <PeacockPatcher.exe> -> в скрытном режиме                      
        process = subprocess.Popen(                                              
            [peacock_path], 
            creationflags = DETACHED_PROCESS,
            startupinfo   = startupinfo
        ) 
    else:                                                                    # <PeacockPatcher.exe> -> без скрытного режима
         process = subprocess.Popen(                                              
            [peacock_path], 
            creationflags = DETACHED_PROCESS
        ) 

    pid_collection["peacock"] = str(process.pid)                              # PID игры <PeacockPatcher.exe>

except:                                                                       # на случай ошибки
    show_error_message(message = phrases[lang][1],
                       title   = phrases[lang][4])
  



try:                                                                          # :[ запуск сервера <Start Server.cmd> ]:
    if SILENT_MODE:                                         
        process = subprocess.Popen(
            ["cmd.exe", "/c", peacock_cmd_path],
            creationflags = CREATE_NO_WINDOW
        )
    else:
        process = subprocess.Popen( 
            ["cmd.exe", "/c", peacock_cmd_path],    
            creationflags = CREATE_NEW_CONSOLE
        )

    pid_collection["server"] = str(process.pid)                               # PID сервера <Start Server.cmd>

except:                                                                       # на случай ошибки
    show_error_message(message = phrases[lang][2],
                       title   = phrases[lang][4])
  
time.sleep(DEFAULT_AWAIT_TIME)                                                # ожидание пока запустится <Start Server.cmd>




try:                                                                          # :[ запуск самой игры <steamclient_loader_x64.exe> ]:
    process = subprocess.Popen(                                              
        [game_path], 
        creationflags=DETACHED_PROCESS
    )
 
    pid_collection["client"] = str(process.pid)                               # PID игры <steamclient_loader_x64.exe>

except:                                                                       # на случай ошибки
    show_error_message(message = phrases[lang][3],
                       title   = phrases[lang][4])

time.sleep(DEFAULT_AWAIT_TIME)                                                # очередное ожидание для запуска <steamclient_loader_x64.exe>




pid_collection["steam_game"] = get_procces_pid(                               # получение PID <HITMAN3.exe> в папке .\HITMAN 3\Retail
        process_name = "HITMAN3",                                             # имя процесса
        procces_path = steam_game_path                                        # путь к процессу
    ) 


pid_collection["nodejs"] = get_procces_pid(                                   # получение PID <node.exe> Nodejs в папке peacock .\peacock\nodedist
        process_name = "node",                                                # имя процесса
        procces_path = peacock_node_path                                      # путь к процессу
    ) 






if pid_collection:                                                                # вывод коллекции PID в <PID_collections.ini>
    for k in pid_collection:
        print(f"[PID]: {k} -> {pid_collection[k]}")                                                                                                       

    try:
        for k in pid_collection:                                                  # Первый этап: вывод обычных PID 
            if k == "steam_game":continue #break                                  # перешагиваем ключ <steam_game> (Костыль)

            update_ini(                                                           # запись PID: <PeacockPatcher.exe>, <steamclient_loader_x64.exe>, <Start Server.cmd>, <node.exe>
                file_path = os.path.join(launcher_settings, PID_INI_FNAME),       # имя файла
                section   = "PID",                                                # секция
                key       = k,                                                    # ключ 
                value     = pid_collection.get(k, "0")                            # значение 
                )

    except Exception as error_message:                                            # на случай ошибки
        show_error_message(message = error_message,
                           title   = phrases[lang][4])
    



    try:
        update_ini(                                                              # запись PID: <HITMAN3.exe>
                file_path = os.path.join(launcher_settings, PID_INI_FNAME),      # имя файла
                section   = "GAME_PID",                                          # секция
                key       = "steam_game",                                        # ключ 
                value     = pid_collection.get("steam_game", "0")                # значение                
                )
        
    except Exception as error_message:                                           # на случай ошибки
        show_error_message(message = error_message,
                           title   = phrases[lang][4])

