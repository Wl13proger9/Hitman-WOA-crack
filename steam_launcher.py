#                                                                                                                                                              
#    LLLLLLLLLLL                                                                                   hhhhhhh                                                     
#    L:::::::::L                                                                                   h:::::h                                                     
#    L:::::::::L                                                                                   h:::::h                                                     
#    LL:::::::LL                                                                                   h:::::h                                                     
#      L:::::L                 aaaaaaaaaaaaa  uuuuuu    uuuuuunnnn  nnnnnnnn        cccccccccccccccch::::h hhhhh           eeeeeeeeeeee    rrrrr   rrrrrrrrr   
#      L:::::L                 a::::::::::::a u::::u    u::::un:::nn::::::::nn    cc:::::::::::::::ch::::hh:::::hhh      ee::::::::::::ee  r::::rrr:::::::::r  
#      L:::::L                 aaaaaaaaa:::::au::::u    u::::un::::::::::::::nn  c:::::::::::::::::ch::::::::::::::hh   e::::::eeeee:::::eer:::::::::::::::::r 
#      L:::::L                          a::::au::::u    u::::unn:::::::::::::::nc:::::::cccccc:::::ch:::::::hhh::::::h e::::::e     e:::::err::::::rrrrr::::::r
#      L:::::L                   aaaaaaa:::::au::::u    u::::u  n:::::nnnn:::::nc::::::c     ccccccch::::::h   h::::::he:::::::eeeee::::::e r:::::r     r:::::r
#      L:::::L                 aa::::::::::::au::::u    u::::u  n::::n    n::::nc:::::c             h:::::h     h:::::he:::::::::::::::::e  r:::::r     rrrrrrr
#      L:::::L                a::::aaaa::::::au::::u    u::::u  n::::n    n::::nc:::::c             h:::::h     h:::::he::::::eeeeeeeeeee   r:::::r            
#      L:::::L         LLLLLLa::::a    a:::::au:::::uuuu:::::u  n::::n    n::::nc::::::c     ccccccch:::::h     h:::::he:::::::e            r:::::r            
#    LL:::::::LLLLLLLLL:::::La::::a    a:::::au:::::::::::::::uun::::n    n::::nc:::::::cccccc:::::ch:::::h     h:::::he::::::::e           r:::::r            
#    L::::::::::::::::::::::La:::::aaaa::::::a u:::::::::::::::un::::n    n::::n c:::::::::::::::::ch:::::h     h:::::h e::::::::eeeeeeee   r:::::r            
#    L::::::::::::::::::::::L a::::::::::aa:::a uu::::::::uu:::un::::n    n::::n  cc:::::::::::::::ch:::::h     h:::::h  ee:::::::::::::e   r:::::r            
#    LLLLLLLLLLLLLLLLLLLLLLLL  aaaaaaaaaa  aaaa   uuuuuuuu  uuuunnnnnn    nnnnnn    cccccccccccccccchhhhhhh     hhhhhhh    eeeeeeeeeeeeee   rrrrrrr            
#                                                                                                                                                                                                          
# (Hitman 3 game launcher) made by - WL13Proger9                                                                                                                                                                       



import os
import time
import locale

import psutil
import ctypes

import subprocess
import configparser




phrases = {                                                             
    "en": {1: "File <./Retail/hitman_launcher.exe> not found! It’s possible that the antivirus deleted it.",    
           2: "Error with file: This file not found."},

    "ru": {1: "Файл <./Retail/hitman_launcher.exe> не найден! Возможно его удалил антивирус.",
           2: "Ошибка с файлом: Данный файл не найден."}
        }
lang = "en"                                                                         # язык


PID_INI_FNAME       = "PID_collections.ini"                                         # имя .ini файла с коллекцией PID
SETTINGS_INI_FNAME  = "launcher_settings.ini"                                       # имя .ini файла с настройками лаунчера

DETACHED_PROCESS = 0x00000008                                                       # windows флаг для независимого запуска
CREATE_NO_WINDOW = 0x08000000                                                       # windows флаг для создания без окна консоли


ab_path                = os.getcwd()                                                # путь к директории обьекта
retail_path            = os.path.join(ab_path, 'Retail')                            # папка Retail

crack_launcher_path    = os.path.join(ab_path, 'Retail', 'hitman_launcher.exe')     # лаунчер кряка
launcher_settings_path = os.path.join(retail_path, 'launcher_settings')             # папка с настройками лаунчера

ini_pid_collections    = os.path.join(launcher_settings_path, PID_INI_FNAME)        # файл коллекции PID               
ini_launcher_settings  = os.path.join(launcher_settings_path, SETTINGS_INI_FNAME)   # файл настроек лаунчера    



def show_error_message(message:str, title:str) -> None:                             # функция для окна ошибок
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)                       # само окно ошибок


def check_ini(file_path:str, section:str, key:str) -> str | None:                   # функция для чтения .ini  
    try:
        config = configparser.ConfigParser()                                        # инициализация парсера                    
        config.read(file_path, encoding='utf-8')                                    # чтение документа

        return config.get(section, key, fallback = None)                            # вывод значение через ключ и секцию
    except: return None                                                             # на случай ошибки


def update_ini(file_path:str, section:str, key:str, value:str) -> None:             # функция для изменение ini файлов   
    config = configparser.ConfigParser()                                            # инициализация парсера 
    config.read(file_path, encoding='utf-8')                                        # чтение документа

    
    config[section][key] = value                                                    # изменение существующего значение, или добавление нового  
    with open(file_path, 'w', encoding='utf-8') as f:                               # применение изменений
        config.write(f)


def startup() -> None:                                                              # функция для начала работы скрипта
    global lang
    os.makedirs(launcher_settings_path, exist_ok=True)                              # костыль опять двадцать пять
    content = """[STARTUP]
silent_mode = true
start_logo  = true
"""

    def _generate_or_check_launcher_settings_ini() -> None:                        # подфункция для файла настроек лаунчера

        if os.path.exists( ini_launcher_settings ):                                # если файлик есть

            ini_silent_mode_value = check_ini(                                  
                                    file_path = ini_launcher_settings, 
                                    section   = "STARTUP", 
                                    key       = "silent_mode"
                                ).lower() == "true"

            ini_start_logo_value= check_ini(                              
                                    file_path = ini_launcher_settings, 
                                    section   = "STARTUP", 
                                    key       = "start_logo").lower() == "true"
            

            print(f"silent_mode - {ini_silent_mode_value}")
            print(f"start_logo - {ini_start_logo_value}")


            if not isinstance(ini_silent_mode_value, bool):
                update_ini(
                            file_path = ini_launcher_settings, 
                            section   = "STARTUP", 
                            key       = "silent_mode",
                            value     = "true"
                )


            if not isinstance(ini_start_logo_value, bool):
                update_ini(
                            file_path = ini_launcher_settings, 
                            section   = "STARTUP", 
                            key       = "start_logo",
                            value     = "true"
                )

            

        else:                                                                      # если его нет
            with open(ini_launcher_settings, "w") as f:   
                f.write(content)
                f.close()


    try:
        os_locale = locale.getlocale()                                             # уровень 1) проверка локализации

        match os_locale[0]:
            case "Russian_Russia": lang = "ru"                                     # русский                                              
            case    _:             lang = "en"                                     # если нет, то английский

    except:pass                                                                    # на случай если нет аргументов



    try:                                                                          # уровень 2) проверка файлика настроек лаунчера
        _generate_or_check_launcher_settings_ini()

    except:
         with open(ini_launcher_settings, "w") as f:   
            f.write(content)
            f.close()

    time.sleep(1)                                                                # ожидание на возможное создание файлика



    try:                                                                         # уровень 3) запуск лаунчера кряка
        subprocess.run(                                                         
            [crack_launcher_path, lang], 
            cwd=retail_path,
            creationflags=CREATE_NO_WINDOW
        ) 

    except:                                                                      # на случай ошибки
        show_error_message(
            message = phrases[lang][1],
            title   = phrases[lang][2]
        )                                                                 
   



startup()                                                                                           # начало алгоритма


steam_game_proc = psutil.Process(int(check_ini( ini_pid_collections, "GAME_PID", "steam_game") ))   #PID: <HITMAN3.exe>
server_proc     = psutil.Process(int(check_ini( ini_pid_collections, "PID", "server")          ))   #PID: <Start Server.cmd>


peacock_proc    = psutil.Process(int(check_ini( ini_pid_collections, "PID", "peacock")         ))   #PID: <PeacockPatcher.exe>
client_proc     = psutil.Process(int(check_ini( ini_pid_collections, "PID", "client")          ))   #PID: <steamclient_loader_x64.exe>

nodejs_proc     = psutil.Process(int(check_ini( ini_pid_collections, "PID", "nodejs")          ))   #PID: <node.exe>


while True:
    time.sleep(2)                                                                                   # ожидание для запуска самой игры

    try:
        if not steam_game_proc.is_running():                                                        # проверка главного <HITMAN3.exe>

            if server_proc.is_running():                                                            # проверка <Start Server.cmd>
                server_proc.terminate()  
                server_proc.kill()  
                print("Kill <Start Server.cmd>")
                

            if peacock_proc.is_running():                                                          # проверка <PeacockPatcher.exe>
                peacock_proc.terminate()  
                peacock_proc.kill() 
                print("Kill <PeacockPatcher.exe>")


            if client_proc.is_running():                                                           # проверка <steamclient_loader_x64.exe>
                client_proc.terminate()  
                client_proc.kill() 
                print("Kill <steamclient_loader_x64.exe>")


            if nodejs_proc.is_running():                                                           # проверка <node.exe>
                nodejs_proc.terminate()  
                nodejs_proc.kill() 
                print("Kill <node.exe>")     
                           
            break    
    except Exception as error_message:
        show_error_message(
            message = error_message,
            title   = phrases[lang][2]
        )                                                                 
           
