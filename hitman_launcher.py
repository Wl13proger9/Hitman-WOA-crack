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
}                                                                           #фразы для ошибок

lang              = "en"                                                    #язык
pid_collection    = {}                                                      #коллекция PID индефикаторов
ab_path           = os.getcwd()                                             #путь к директории обьекта


peacock_path      = os.path.join(ab_path, 'peacock', 'PeacockPatcher.exe')  #взломанный патчер Peacock
peacock_cmd_path  = os.path.join(ab_path, 'peacock', 'Start Server.cmd')    #взломанный сервер Peacock


game_path         = os.path.join(ab_path, 'steamclient_loader_x64.exe')     #взломанный клиент игры
steam_game_path   = os.path.join(ab_path, 'HITMAN3.exe')                    #сама игра
launcher_settings = os.path.join(ab_path, 'launcher_settings')              #папка настроек лаунчера


DETACHED_PROCESS = 0x00000008                                               #windows флаг для независимого запуска
CREATE_NO_WINDOW = 0x08000000                                               #windows флаг для создания без окна консоли





                                                           
try:
    argv = sys.argv[1]                                                      #аргументы

    match argv:
        case "ru": lang = "ru"                                              #русский
        case "en": lang = "en"                                              #английский
        case    _: lang = "en"

except:pass                                                                 #на случай если нет аргументов



def _show_error_message(message:str, title:str) -> None:                    #функция для окна ошибок
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)


def _update_ini(file_path:str, section:str, key:str, value:str) -> None:    #функция для изменение ini файлов   
    config = configparser.ConfigParser()                                    #инициализация парсера 
    config.read(file_path, encoding='utf-8')                                #чтение документа

    
    config[section][key] = value                                            #изменение существующего значение, или добавление нового                                                               
    with open(file_path, 'w', encoding='utf-8') as f:                       #применение изменений
        config.write(f)




def _get_steamgame_pid(steam_game:str) -> str:                              #функция для взятия PID самой игры
    command = f"Get-Process -Name HITMAN3 | Where-Object {{ $_.Path -eq '{steam_game}' }} | Select-Object Id"

    result = subprocess.run(
        [ "powershell", "-Command", command ],                              #исполнение команды через Powershell
        capture_output=True,
        text=True,
        encoding="cp866",
        creationflags=CREATE_NO_WINDOW
        ).stdout

    return re.findall(r'\d+', result)[0]                                   #парсинг данных вывода


def _startup() -> None:
    os.makedirs(launcher_settings, exist_ok=True)                          #создание папки настроек ланучера
    content = """[PID]                                  
peacock= 
server= 
client= 

[GAME_PID]
steam_game=
"""

    with open(os.path.join( launcher_settings, "PID_collections.ini" ),    #создания списка PID
            "w", encoding="utf-8") as f:
        f.write(content)
        f.close()
 


_startup()                                                                  #начала алгоритма 



try:
    process = subprocess.Popen(                                             #запуск патчера
        [peacock_path], 
        creationflags=DETACHED_PROCESS
    ) 

    pid_collection["peacock"] = str(process.pid)                            #PID игры <PeacockPatcher.exe>
except:                                                                     #на случай ошибки
    _show_error_message(message = phrases[lang][1],
                        title   = phrases[lang][4])

    

try:                                                                        #запуск сервера
    process = subprocess.Popen(
        ["cmd.exe", "/c", peacock_cmd_path],
        creationflags=CREATE_NO_WINDOW
    )

    pid_collection["server"] = str(process.pid)                             #PID сервера <Start Server.cmd>
except:                                                                     #на случай ошибки
    _show_error_message(message = phrases[lang][2],
                        title   = phrases[lang][4])
  


time.sleep(0.3)                                                             #ожидание в 0.3 секунды



try:
    process = subprocess.Popen(                                             #запуск самой игры
        [game_path], 
        creationflags=DETACHED_PROCESS
    )

    
    pid_collection["client"] = str(process.pid)                             #PID игры <steamclient_loader_x64.exe>
except:                                                                     #на случай ошибки
    _show_error_message(message = phrases[lang][3],
                        title   = phrases[lang][4])




time.sleep(0.3)                                                             #очередное ожидание в 0.3 секунды
pid_collection["steam_game"] = _get_steamgame_pid(steam_game_path) 



if pid_collection:
        print(pid_collection)                                                   #вывод коллекции PID

    #try:
        for k in pid_collection:
            if k == "steam_game":break
            _update_ini(                                                    #запись PID <PeacockPatcher.exe>
                file_path = os.path.join(launcher_settings, "PID_collections.ini"),
                section   = "PID", 
                key       = k, 
                value     = pid_collection.get(k, "0")                   
                )



    #except Exception as e:pass
        #print(e)
        



    #try:
        _update_ini(                                                         #запись PID <HITMAN3.exe>
                file_path = os.path.join(launcher_settings, "PID_collections.ini"),
                section   = "GAME_PID", 
                key       = "steam_game", 
                value     = pid_collection.get("steam_game", "0")                   
                )
    #except Exception as e:pass
            #print(e)

