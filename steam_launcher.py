#                                                                                                                                                                                                             
#       SSSSSSSSSSSSSSS TTTTTTTTTTTTTTTTTTTTTTT     LLLLLLLLLLL                                                                                   hhhhhhh                                                     
#     SS:::::::::::::::ST:::::::::::::::::::::T     L:::::::::L                                                                                   h:::::h                                                     
#    S:::::SSSSSS::::::ST:::::::::::::::::::::T     L:::::::::L                                                                                   h:::::h                                                     
#    S:::::S     SSSSSSST:::::TT:::::::TT:::::T     LL:::::::LL                                                                                   h:::::h                                                     
#    S:::::S            TTTTTT  T:::::T  TTTTTT       L:::::L                 aaaaaaaaaaaaa  uuuuuu    uuuuuunnnn  nnnnnnnn        cccccccccccccccch::::h hhhhh           eeeeeeeeeeee    rrrrr   rrrrrrrrr   
#    S:::::S                    T:::::T               L:::::L                 a::::::::::::a u::::u    u::::un:::nn::::::::nn    cc:::::::::::::::ch::::hh:::::hhh      ee::::::::::::ee  r::::rrr:::::::::r  
#     S::::SSSS                 T:::::T               L:::::L                 aaaaaaaaa:::::au::::u    u::::un::::::::::::::nn  c:::::::::::::::::ch::::::::::::::hh   e::::::eeeee:::::eer:::::::::::::::::r 
#      SS::::::SSSSS            T:::::T               L:::::L                          a::::au::::u    u::::unn:::::::::::::::nc:::::::cccccc:::::ch:::::::hhh::::::h e::::::e     e:::::err::::::rrrrr::::::r
#        SSS::::::::SS          T:::::T               L:::::L                   aaaaaaa:::::au::::u    u::::u  n:::::nnnn:::::nc::::::c     ccccccch::::::h   h::::::he:::::::eeeee::::::e r:::::r     r:::::r
#           SSSSSS::::S         T:::::T               L:::::L                 aa::::::::::::au::::u    u::::u  n::::n    n::::nc:::::c             h:::::h     h:::::he:::::::::::::::::e  r:::::r     rrrrrrr
#                S:::::S        T:::::T               L:::::L                a::::aaaa::::::au::::u    u::::u  n::::n    n::::nc:::::c             h:::::h     h:::::he::::::eeeeeeeeeee   r:::::r            
#                S:::::S        T:::::T               L:::::L         LLLLLLa::::a    a:::::au:::::uuuu:::::u  n::::n    n::::nc::::::c     ccccccch:::::h     h:::::he:::::::e            r:::::r            
#    SSSSSSS     S:::::S      TT:::::::TT           LL:::::::LLLLLLLLL:::::La::::a    a:::::au:::::::::::::::uun::::n    n::::nc:::::::cccccc:::::ch:::::h     h:::::he::::::::e           r:::::r            
#    S::::::SSSSSS:::::S      T:::::::::T           L::::::::::::::::::::::La:::::aaaa::::::a u:::::::::::::::un::::n    n::::n c:::::::::::::::::ch:::::h     h:::::h e::::::::eeeeeeee   r:::::r            
#    S:::::::::::::::SS       T:::::::::T           L::::::::::::::::::::::L a::::::::::aa:::a uu::::::::uu:::un::::n    n::::n  cc:::::::::::::::ch:::::h     h:::::h  ee:::::::::::::e   r:::::r            
#     SSSSSSSSSSSSSSS         TTTTTTTTTTT           LLLLLLLLLLLLLLLLLLLLLLLL  aaaaaaaaaa  aaaa   uuuuuuuu  uuuunnnnnn    nnnnnn    cccccccccccccccchhhhhhh     hhhhhhh    eeeeeeeeeeeeee   rrrrrrr            
#                                                                                                                                                                                                             
# (Steam launcher) made by - WL13Proger9                                                                                                                                                                       



import os
import locale

import ctypes
import subprocess








phrases = {
    "en": {
            1: "File <./Retail/hitman_launcher.exe> not found! It’s possible that the antivirus deleted it.",    

            2: "Error with file: This file not found.",
        },

    "ru": {
            1: "Файл <./Retail/hitman_launcher.exe> не найден! Возможно его удалил антивирус.",

            2: "Ошибка с файлом: Данный файл не найден.",
    }
}




lang = "en"                                                                     #язык

try:
    os_locale = locale.getlocale()

    match os_locale[0]:
        case "Russian_Russia": lang = "ru"                                      #русский                                              
        case    _:             lang = "en"                                      #если нет, то английский

except:pass                                                                     #на случай если нет аргументов





ab_path = os.getcwd()                                                           #путь к директории обьекта
crack_launcher_path = os.path.join(ab_path, 'Retail', 'hitman_launcher.exe')    #лаунчер кряка
retail_path         = os.path.join(ab_path, 'Retail')                           #папка Retail


DETACHED_PROCESS = 0x00000008                                                   #windows флаг для независимого запуска
CREATE_NO_WINDOW = 0x08000000                                                   #windows флаг для создания без окна консоли



try:
    subprocess.Popen(                                                           #запуск лаунчера кряка
        [crack_launcher_path, lang], 
        cwd=retail_path,
        creationflags=DETACHED_PROCESS
    ) 

except:                                                                         #на случай ошибки
    ctypes.windll.user32.MessageBoxW(
                                    0,
                                    phrases[lang][1],                           #сообщение ошибки
                                    phrases[lang][2],                           #название окна ошибки
                                    0x10
                                    )        
    


    