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
# Module

import os
import zipfile

import shutil
import requests

from  .path_files import get_steam_path



def download_crack_from_github(output_path:str = ".", file_name:str = "crack.zip") -> None | str:
    try:
        repo_link = "https://github.com/Wl13proger9/Hitman-WOA-crack"            #нужные ссылки
        crack_link = "https://github.com/Wl13proger9/Hitman-WOA-crack/releases/download/important/crack.zip"    



        if requests.head(repo_link).status_code == 200:                          #проверка, существует ли ещё репозиторий
            file_content = requests.get(crack_link).content                      #скачивание архива по ссылке через релизы

            with open(os.path.join(output_path, file_name), 'wb') as f:          #установка архива в нужную директорию
                f.write(file_content)   


    except Exception as e: return e



def unpack_crack_archive(file_name:str, output_path:str = ".") -> None | str:
    try:
        with zipfile.ZipFile(file_name, 'r') as zip:                            #чтение архива
            zip.extractall(output_path)                                         #распаковка архива

    except Exception as e: return e                                             #на случай ошибки
    
  

def inject_crack_in_game(game_path:str = None) -> None:

    if game_path == None:                                                       #если папка не задана, то по дефолту
        game_path = os.path.join(get_steam_path(), 
                                "steamapps", "common",                      
                                "HITMAN 3", "test") #Retail

    crack_path   = "./crack"
    crack_folder = [
                    ["peacock", "steam_settings"],                             #папки. Индекс 0

                    [                                                          
                    "ColdClientLoader.ini", 
                    "steamclient_loader_x64.exe",       
                    "GameOverlayRenderer.dll",                                 #файлы. Индекс 1
                    "GameOverlayRenderer64.dll",
                    "steamclient.dll",
                    "steamclient64.dll"
                    ]
    ]


    if os.path.exists( game_path ):
        crack_paths, crack_files = crack_folder[0], crack_folder[1]

        for path in crack_paths:
            shutil.copytree( 
                            os.path.join(crack_path, path), 
                            os.path.join(game_path,  path), 
                            dirs_exist_ok=True
                            )

        for file in crack_files:
            shutil.copy( 
                        os.path.join(crack_path, file), 
                        os.path.join(game_path,  file), 
                        )






if __name__ == "__main__":
    #download_crack_from_github() 
    #unpack_crack_archive()

    inject_crack_in_game()
